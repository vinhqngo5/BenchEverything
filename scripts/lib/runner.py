# scripts/lib/runner.py

import subprocess
import os
import shutil
import platform
from pathlib import Path
from typing import Dict, Tuple, Optional, List # Added List

from .logger import get_logger
from .config import BenchEverythingConfig
from .environment import extract_compiler_from_toolchain, get_compiler_version
from .metadata import create_metadata_dict, save_metadata, load_metadata
from .assembly import AssemblyExtractor

logger = get_logger()

class BuildError(Exception):
    """Custom exception for build failures."""
    pass

class BenchmarkExecutionError(Exception):
    """Custom exception for benchmark execution failures."""
    pass


class BenchmarkRunner:
    """Handles building and running benchmarks."""

    def __init__(self, config: BenchEverythingConfig):
        self.config = config
        self.project_root = config.get_project_root()

    # ... (keep _determine_build_params and build_experiment as they are) ...
    def _determine_build_params(self, build_flags_id: str) -> Tuple[str, str]:
        """Determine CMake build type and CXX flags from the build_flags_id."""
        # Defaults
        cmake_build_type = "Release"
        opt_flag = "-O3" # Default optimization
        arch_flag = ""

        flags_lower = build_flags_id.lower()

        # Determine Build Type
        if "relwithdebinfo" in flags_lower:
            cmake_build_type = "RelWithDebInfo"
        elif "release" in flags_lower:
            cmake_build_type = "Release"
        elif "debug" in flags_lower:
            cmake_build_type = "Debug"
            opt_flag = "-O0" # Debug usually means O0

        # Determine Optimization Level
        if "_o3" in flags_lower: opt_flag = "-O3"
        elif "_o2" in flags_lower: opt_flag = "-O2"
        elif "_o1" in flags_lower: opt_flag = "-O1"
        elif "_o0" in flags_lower: opt_flag = "-O0"
        elif "_os" in flags_lower: opt_flag = "-Os" # Optimize for size
        elif "_oz" in flags_lower: opt_flag = "-Oz" # Optimize more for size

        # Determine Arch Flags
        if "_native" in flags_lower: arch_flag = "-march=native"
        # Add more specific arch flags if needed (e.g., _avx2, _avx512)
        elif "_avx2" in flags_lower: arch_flag = "-mavx2"
        elif "_avx512f" in flags_lower: arch_flag = "-mavx512f" # Example

        # Combine flags (ensure std is always present)
        cxx_flags = f"-std=c++20 {opt_flag} {arch_flag}".strip()
        logger.info(f"Determined build params for '{build_flags_id}': "
                    f"CMake Type='{cmake_build_type}', CXX Flags='{cxx_flags}'")
        return cmake_build_type, cxx_flags

    def build_experiment(self, compiler_name: str, build_flags_id: str, incremental: bool) -> Optional[Path]:
        """
        Configure and build all experiments for a given compiler and build flags.

        Returns:
            The Path to the build directory if successful, None otherwise.
        """
        logger.info(f"Building experiments with compiler '{compiler_name}' and flags '{build_flags_id}'...")

        compiler_config = self.config.get_compiler_config(compiler_name)
        if not compiler_config:
            logger.error(f"Compiler config for '{compiler_name}' not found.")
            return None

        # Generate metadata first to get detailed IDs needed for paths
        # Need to pass dummy values for hash/source generation, they aren't used for path determination here
        try:
             # Pass dummy command base needed by create_metadata_dict
            dummy_gbench_cmd_base = ["dummy_executable"]
            metadata_template = create_metadata_dict(
                self.config, "dummy_experiment", compiler_config, build_flags_id,
                 "dummy_flags", "dummy_type", dummy_gbench_cmd_base
            )
            detailed_platform_id = metadata_template['detailed_platform_id']
            detailed_compiler_id = metadata_template['detailed_compiler_id']
        except Exception as e:
             logger.error(f"Failed to pre-determine platform/compiler IDs for build path: {e}", exc_info=True) # Add traceback
             # Fallback to simpler names if detailed ID generation fails
             logger.warning("Using fallback platform/compiler IDs for build path.")
             detailed_platform_id = f"{platform.system().lower()}-{platform.machine()}" # <<< FIXED: Was causing NameError
             detailed_compiler_id = compiler_name # Use the name from config

        build_dir = self.config.get_build_dir(detailed_platform_id, detailed_compiler_id, build_flags_id)

        # Clean build directory if not incremental
        if not incremental and build_dir.exists():
            logger.info(f"Cleaning build directory: {build_dir}")
            try:
                shutil.rmtree(build_dir)
            except OSError as e:
                 logger.error(f"Failed to clean build directory {build_dir}: {e}")
                 # Continue? Or fail hard? Let's try continuing.
                 pass # Try to proceed even if cleanup fails

        os.makedirs(build_dir, exist_ok=True)

        # Determine CMake build type and CXX flags from build_flags_id
        cmake_build_type, cxx_flags = self._determine_build_params(build_flags_id)

        # Run CMake configure
        toolchain_path = self.project_root / compiler_config['toolchain_file']
        if not toolchain_path.exists():
             logger.error(f"Toolchain file not found: {toolchain_path}")
             return None

        cmake_cmd = [
            "cmake",
            "-S", str(self.project_root),
            "-B", str(build_dir),
            f"-DCMAKE_TOOLCHAIN_FILE={toolchain_path}",
            f"-DCMAKE_BUILD_TYPE={cmake_build_type}",
            f"-DCMAKE_CXX_FLAGS={cxx_flags}"
        ]

        # Add experiment-specific CMake flags (currently global, needs refinement if truly per-exp)
        # all_experiments = self.config.get_all_experiment_names()
        # for exp_name in all_experiments:
        #      exp_config = self.config.load_experiment_config(exp_name)
        #      if exp_config.get("cmake_flags"):
        #           cmake_cmd.append(exp_config["cmake_flags"]) # This might apply flags globally

        logger.info(f"Running CMake configure: {' '.join(cmake_cmd)}")
        try:
            # Capture output for better error reporting
            result = subprocess.run(cmake_cmd, check=True, capture_output=True, text=True, cwd=build_dir, timeout=180)
            logger.debug(f"CMake Configure Output:\n{result.stdout[-1000:]}") # Log last 1k lines
            if result.stderr:
                 logger.warning(f"CMake Configure Stderr:\n{result.stderr[-1000:]}")
        except subprocess.CalledProcessError as e:
            logger.error(f"CMake configure failed (return code {e.returncode})")
            logger.error(f"Stdout:\n{e.stdout}")
            logger.error(f"Stderr:\n{e.stderr}")
            return None
        except subprocess.TimeoutExpired:
             logger.error("CMake configure timed out.")
             return None
        except Exception as e:
            logger.error(f"Unexpected error during CMake configure: {e}", exc_info=True)
            return None

        # Run CMake build
        build_cmd = ["cmake", "--build", str(build_dir), "--parallel"] # Use parallel build
        logger.info(f"Running CMake build: {' '.join(build_cmd)}")
        try:
            result = subprocess.run(build_cmd, check=True, capture_output=True, text=True, cwd=build_dir, timeout=600) # 10 min timeout
            logger.debug(f"CMake Build Output:\n{result.stdout[-1000:]}")
            if result.stderr:
                 logger.warning(f"CMake Build Stderr:\n{result.stderr[-1000:]}")
            logger.info("Build completed successfully.")
            return build_dir
        except subprocess.CalledProcessError as e:
            logger.error(f"CMake build failed (return code {e.returncode})")
            logger.error(f"Build Stdout:\n{e.stdout}")
            logger.error(f"Build Stderr:\n{e.stderr}")
            raise BuildError(f"CMake build failed for {compiler_name} ({build_flags_id})")
        except subprocess.TimeoutExpired:
             logger.error("CMake build timed out.")
             raise BuildError(f"CMake build timed out for {compiler_name} ({build_flags_id})")
        except Exception as e:
            logger.error(f"Unexpected error during CMake build: {e}", exc_info=True)
            raise BuildError(f"Unexpected build error for {compiler_name} ({build_flags_id})")


    def run_experiment(self, experiment_name: str, compiler_name: str, build_flags_id: str, build_dir: Path, force: bool) -> Tuple[Optional[Path], str]:
        """
        Run a specific benchmark experiment, collect results, and save metadata.

        Returns:
            Tuple of (Optional[Path], status_string).
            Path is the results directory if successful/skipped.
            Status string is one of: "RAN", "SKIPPED", "FAILED".
            Returns (None, "FAILED") on critical pre-run errors.
        """
        status = "FAILED" # Default status
        results_dir = None # Initialize results_dir

        try:
            logger.info(f"--- Running Experiment: {experiment_name} ({compiler_name}, {build_flags_id}) ---")

            exp_details = self.config.get_experiment_details(experiment_name)
            if not exp_details:
                logger.error(f"Experiment details not found for '{experiment_name}' in global config.")
                return None, "FAILED"
            benchmark_executable_name = exp_details.get('benchmark_executable')
            if not benchmark_executable_name:
                logger.error(f"Missing 'benchmark_executable' for experiment '{experiment_name}' in config.")
                return None, "FAILED"

            compiler_config = self.config.get_compiler_config(compiler_name)
            if not compiler_config:
                 logger.error(f"Compiler config for {compiler_name} not found during run phase.")
                 return None, "FAILED"

            # --- Determine Output Path & Generate Metadata ---
            cmake_build_type, cxx_flags_used = self._determine_build_params(build_flags_id)
            benchmark_exe_path = build_dir / "experiments" / experiment_name / benchmark_executable_name
            gbench_cmd_base = [str(benchmark_exe_path)] # Base command

            # Check for executable existence early
            if not benchmark_exe_path.exists():
                logger.error(f"Benchmark executable not found: {benchmark_exe_path}")
                return None, "FAILED"

            try:
                metadata = create_metadata_dict(
                    self.config, experiment_name, compiler_config, build_flags_id,
                    cxx_flags_used, cmake_build_type, gbench_cmd_base
                )
                metadata_hash = metadata['metadata_hash']
                detailed_platform_id = metadata['detailed_platform_id']
                detailed_compiler_id = metadata['detailed_compiler_id']
            except Exception as e:
                logger.error(f"Failed to generate metadata for {experiment_name}: {e}", exc_info=True)
                return None, "FAILED"

            results_dir = self.config.get_results_dir(
                detailed_platform_id, detailed_compiler_id, build_flags_id, metadata_hash, experiment_name
            )

            # --- Check Force / Existing Results ---
            if results_dir.exists() and not force:
                logger.warning(f"Results directory already exists: {results_dir}")
                existing_metadata = load_metadata(results_dir)
                if existing_metadata and existing_metadata.get('metadata_hash') == metadata_hash:
                     # Check if essential output file also exists
                     if (results_dir / "benchmark_output.json").exists():
                          logger.info("Valid results exist and metadata hash matches. Skipping run.")
                          return results_dir, "SKIPPED" # <<< Explicitly return SKIPPED status
                     else:
                          logger.warning("Metadata matches, but benchmark output missing. Overwriting.")
                          # Proceed to run
                else:
                     logger.warning("Existing metadata hash mismatch or metadata missing. Overwriting.")
                     # Proceed to run

            # --- Proceed with Execution ---
            logger.info(f"Proceeding with benchmark run for {experiment_name}. Output: {results_dir}")
            os.makedirs(results_dir, exist_ok=True)

            benchmark_output_file = results_dir / "benchmark_output.json"

            exp_config = self.config.load_experiment_config(experiment_name)
            gbench_args = exp_config.get("gbench_args", "").split()

            json_benchmark_cmd = [str(benchmark_exe_path), "--benchmark_format=json", f"--benchmark_out={benchmark_output_file}"] + gbench_args

            # Run JSON output command
            logger.info(f"Running benchmark (JSON): {' '.join(json_benchmark_cmd)}")
            result_json = subprocess.run(json_benchmark_cmd, check=True, capture_output=True, text=True, cwd=results_dir, timeout=600)

            # Check if JSON file was actually created and is not empty
            if not benchmark_output_file.exists() or benchmark_output_file.stat().st_size == 0:
                 logger.error(f"Benchmark ran but JSON output file is missing or empty: {benchmark_output_file}")
                 logger.error(f"Benchmark stdout:\n{result_json.stdout}")
                 logger.error(f"Benchmark stderr:\n{result_json.stderr}")
                 raise BenchmarkExecutionError("Benchmark JSON output file empty/missing.")

            # --- Run Perf Stat (Linux only) ---
            if platform.system() == "Linux":
                self._run_perf_stat(results_dir, json_benchmark_cmd, exp_config)
            else:
                logger.info("Skipping perf stat (not on Linux).")

            # --- Extract Assembly ---
            try:
                 extractor = AssemblyExtractor(build_dir, experiment_name, benchmark_executable_name, self.project_root)
                 extractor.extract_assembly(results_dir, build_flags_id)
            except Exception as e:
                 logger.error(f"Assembly extraction failed: {e}", exc_info=True)
                 # Continue without assembly

            # --- Save Metadata ---
            if not save_metadata(metadata, results_dir):
                logger.error("Failed to save metadata file.")
                # Continue but maybe log a higher severity warning?

            logger.info(f"--- Experiment {experiment_name} completed successfully. Results: {results_dir} ---")
            status = "RAN" # <<< Explicitly set RAN status on success
            return results_dir, status

        except subprocess.CalledProcessError as e:
            logger.error(f"Benchmark execution failed (return code {e.returncode})")
            logger.error(f"Command: {' '.join(e.cmd)}")
            logger.error(f"Stdout:\n{e.stdout}")
            logger.error(f"Stderr:\n{e.stderr}")
            # Raise specific error to be caught by caller
            raise BenchmarkExecutionError(f"Benchmark execution failed for {experiment_name}") from e
        except subprocess.TimeoutExpired:
            logger.error("Benchmark execution timed out.")
            raise BenchmarkExecutionError(f"Benchmark execution timed out for {experiment_name}")
        except BenchmarkExecutionError as e: # Catch specific error from checks
             logger.error(f"Benchmark execution error: {e}")
             raise # Re-raise to be caught by caller
        except Exception as e:
            logger.error(f"Unexpected error running benchmark {experiment_name}: {e}", exc_info=True)
            raise BenchmarkExecutionError(f"Unexpected error running benchmark for {experiment_name}") from e

        # This part should ideally not be reached if exceptions are raised properly
        # But as a fallback, return FAILED status
        return results_dir, status # results_dir might be None here


    def _run_perf_stat(self, results_dir: Path, benchmark_cmd: list, exp_config: Dict):
        """Run perf stat for the benchmark command."""
        perf_path = shutil.which("perf")
        if not perf_path:
            logger.warning("perf command not found, skipping performance counters.")
            return

        perf_stat_file = results_dir / "perf_stat.log"
        perf_events = "cycles,instructions,cache-references,cache-misses,branch-instructions,branch-misses"
        if exp_config and "perf_events" in exp_config:
             if isinstance(exp_config["perf_events"], list): perf_events = ",".join(exp_config["perf_events"])
             elif isinstance(exp_config["perf_events"], str): perf_events = exp_config["perf_events"]
             logger.info(f"Using custom perf events: {perf_events}")

        perf_cmd = [perf_path, "stat", "-o", str(perf_stat_file), "-e", perf_events, "--"] + benchmark_cmd

        logger.info(f"Running perf stat: {' '.join(perf_cmd)}")
        try:
            subprocess.run(perf_cmd, check=True, capture_output=True, text=True, cwd=results_dir, timeout=900)
            logger.info(f"Performance counters collected with perf stat, saved to {perf_stat_file}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Perf stat failed (return code {e.returncode}). Check {perf_stat_file} for details.")
            if e.stderr: logger.warning(f"Perf stderr:\n{e.stderr[:1000]}...")
        except FileNotFoundError: logger.warning("perf command not found during execution.")
        except subprocess.TimeoutExpired: logger.warning("Perf stat command timed out.")
        except Exception as e: logger.warning(f"Error running perf stat: {e}")