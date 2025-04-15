#!/usr/bin/env python3

import os
import json
import subprocess
import platform
import argparse
import sys
import datetime
import glob
import shutil
import hashlib
import logging
from pathlib import Path
from colorama import init, Fore, Style
import re

# Initialize colorama
init(autoreset=True)

# Configure logging with colors
def setup_logger():
    """Configure a colored logger."""
    logger = logging.getLogger("BenchEverything")
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Custom formatter with colors
    class ColoredFormatter(logging.Formatter):
        FORMATS = {
            logging.DEBUG: Fore.CYAN + "%(levelname)s: %(message)s" + Style.RESET_ALL,
            logging.INFO: "%(message)s",
            logging.WARNING: Fore.YELLOW + "WARNING: %(message)s" + Style.RESET_ALL,
            logging.ERROR: Fore.RED + "ERROR: %(message)s" + Style.RESET_ALL,
            logging.CRITICAL: Fore.RED + Style.BRIGHT + "CRITICAL: %(message)s" + Style.RESET_ALL
        }
        
        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)
    
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)
    return logger

# Set up the logger
logger = setup_logger()

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_cpu_info():
    """Get CPU information across different platforms."""
    cpu_info = "unknown"
    
    if platform.system() == "Darwin":  # macOS
        try:
            cpu_info = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=False
            ).stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to platform.processor if sysctl fails
            cpu_info = platform.processor() or "unknown-mac"
    
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("model name"):
                        cpu_info = line.split(":", 1)[1].strip()
                        break
        except (IOError, FileNotFoundError):
            # Fall back to platform.processor if /proc/cpuinfo can't be read
            cpu_info = platform.processor() or "unknown-linux"
    
    else:  # Windows or other
        cpu_info = platform.processor() or "unknown"
    
    # Clean up and normalize CPU info (remove extra spaces, etc.)
    cpu_info = " ".join(cpu_info.split())
    
    # Further simplify for path use - keep only essential information
    # Remove frequency information which can vary
    cpu_info = re.sub(r'\s+@\s+\d+\.\d+GHz', '', cpu_info)
    # Remove common CPU prefixes/suffixes to keep it shorter
    cpu_info = cpu_info.replace("Intel(R) Core(TM) ", "")
    cpu_info = cpu_info.replace("AMD ", "")
    
    # Replace spaces and special characters with hyphens for path safety
    cpu_info = re.sub(r'[^a-zA-Z0-9-]', '-', cpu_info)
    # Remove consecutive hyphens
    cpu_info = re.sub(r'-+', '-', cpu_info)
    # Remove leading/trailing hyphens
    cpu_info = cpu_info.strip('-')
    
    return cpu_info

def get_compiler_version(compiler_name):
    """Get the compiler version."""
    version = "unknown"
    
    if compiler_name.lower() == "gcc":
        try:
            result = subprocess.run(
                ["g++", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                # Extract version like 11.2.0 from output
                version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
                if version_match:
                    version = version_match.group(1)
                else:
                    # Fallback to first line if regex doesn't match
                    version = result.stdout.split('\n')[0].strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    elif compiler_name.lower() == "clang":
        try:
            result = subprocess.run(
                ["clang++", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                # Extract version like 14.0.0 from output
                version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
                if version_match:
                    version = version_match.group(1)
                else:
                    # Fallback to first line if regex doesn't match
                    version = result.stdout.split('\n')[0].strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    # Clean up version for path use
    version = re.sub(r'[^a-zA-Z0-9\.-]', '-', version)
    
    return version

def generate_metadata_hash(compiler_name, build_flags_id, additional_metadata=None):
    """Generate a hash based on metadata.
    
    Args:
        compiler_name: The compiler name (e.g., 'gcc', 'clang')
        build_flags_id: Build flags identifier (e.g., 'Release_O3')
        additional_metadata: Optional dictionary containing additional metadata to include in the hash
        
    Returns:
        Tuple of (short_hash, metadata_str, detailed_platform_id)
    """
    # Get system information
    system = platform.system().lower()
    machine = platform.machine()
    cpu = get_cpu_info()
    compiler_version = get_compiler_version(compiler_name)
    
    # Create metadata dictionary with standard fields
    metadata = {
        "system": system,
        "machine": machine,
        "cpu": cpu,
        "compiler_name": compiler_name,
        "compiler_version": compiler_version,
        "build_flags_id": build_flags_id
    }
    
    # Add any additional metadata
    if additional_metadata:
        metadata.update(additional_metadata)
    
    # Create a sorted representation for consistent hashing
    metadata_items = sorted(metadata.items())
    
    # Create a string representation of the metadata
    metadata_str = ":".join(f"{k}={v}" for k, v in metadata_items)
    
    # Generate a short hash (8 characters)
    hash_obj = hashlib.md5(metadata_str.encode())
    short_hash = hash_obj.hexdigest()[:8]
    
    # Create a more detailed platform ID for directory structure
    detailed_platform_id = f"{system}-{machine}-{cpu}"
    
    # Create a compiler id that includes version
    detailed_compiler_id = f"{compiler_name}-{compiler_version}"
    
    return short_hash, metadata_str, detailed_platform_id, detailed_compiler_id

def get_system_info():
    """Get detailed system information."""
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    
    # Get CPU info on Linux
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpu_info = f.read()
            system_info["cpu_info"] = cpu_info
        except (IOError, FileNotFoundError):
            system_info["cpu_info"] = "Could not read /proc/cpuinfo"
    
    # Get compiler versions
    try:
        # GCC version
        gcc_result = subprocess.run(
            ["g++", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        system_info["gcc_version"] = gcc_result.stdout.strip().split('\n')[0] if gcc_result.returncode == 0 else "Not available"
        
        # Clang version
        clang_result = subprocess.run(
            ["clang++", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        system_info["clang_version"] = clang_result.stdout.strip().split('\n')[0] if clang_result.returncode == 0 else "Not available"
    except FileNotFoundError:
        system_info["compiler_info"] = "Could not determine compiler versions"
        
    return system_info

def load_config(config_file=None):
    """Load benchmark configuration from JSON file."""
    if config_file:
        config_path = Path(config_file)
    else:
        config_path = PROJECT_ROOT / "scripts" / "config" / "benchmark_config.json"
    
    with open(config_path, 'r') as f:
        return json.load(f)

def get_experiment_config(experiment_name):
    """Load experiment-specific configuration, if it exists."""
    exp_config_path = PROJECT_ROOT / "experiments" / experiment_name / "exp_config.json"
    if exp_config_path.exists():
        with open(exp_config_path, 'r') as f:
            return json.load(f)
    return {}

def build_benchmark(compiler_config, build_flags_id="Release_O3", incremental=False):
    """Build the benchmark using the specified compiler configuration."""
    logger.info(f"Building with {compiler_config['name']}...")
    
    # Generate a hash based on metadata to ensure consistency with run_benchmark
    _, _, detailed_platform_id, detailed_compiler_id = generate_metadata_hash(
        compiler_config['name'], 
        build_flags_id
    )
    
    # Create build directory with more detailed path using the detailed platform ID and compiler ID
    build_dir = PROJECT_ROOT / "build" / detailed_platform_id / detailed_compiler_id / build_flags_id
    
    # Clean build directory if not incremental
    if not incremental and build_dir.exists():
        logger.info(f"Cleaning build directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    os.makedirs(build_dir, exist_ok=True)
    
    # Determine CMake build type and flags
    cmake_build_type = "Release" if "Release" in build_flags_id else "Debug"
    cxx_flags = "-std=c++20"
    
    if "O3" in build_flags_id:
        cxx_flags += " -O3"
    elif "O2" in build_flags_id:
        cxx_flags += " -O2"
    elif "O1" in build_flags_id:
        cxx_flags += " -O1"
    elif "O0" in build_flags_id:
        cxx_flags += " -O0"
    
    if "native" in build_flags_id:
        cxx_flags += " -march=native"
    
    # Run CMake configure
    cmake_cmd = [
        "cmake", "-S", str(PROJECT_ROOT), 
        "-B", str(build_dir),
        f"-DCMAKE_TOOLCHAIN_FILE={PROJECT_ROOT / compiler_config['toolchain_file']}",
        f"-DCMAKE_BUILD_TYPE={cmake_build_type}",
        f"-DCMAKE_CXX_FLAGS={cxx_flags}"
    ]
    
    logger.info(f"Running CMake command: {' '.join(cmake_cmd)}")
    subprocess.run(cmake_cmd, check=True)
    
    # Run CMake build
    build_cmd = ["cmake", "--build", str(build_dir), "--parallel"]
    subprocess.run(build_cmd, check=True)
    
    return build_dir, cxx_flags, cmake_build_type

def create_metadata(experiment, compiler_config, build_flags_id, cxx_flags, cmake_build_type, metadata_hash, metadata_str, detailed_platform_id, detailed_compiler_id):
    """Create metadata JSON for the experiment run."""
    system_info = get_system_info()
    
    # Additional CPU specific information 
    cpu_info = get_cpu_info()
    
    # Extract compiler version for easier access in reports
    compiler_version = get_compiler_version(compiler_config['name'])
    
    timestamp = datetime.datetime.now().isoformat()
    
    metadata = {
        "timestamp_iso": timestamp,
        "metadata_hash": metadata_hash,
        "metadata_source": metadata_str,
        "detailed_platform_id": detailed_platform_id,
        "detailed_compiler_id": detailed_compiler_id,
        "platform_id": f"{platform.system().lower()}-{platform.machine()}",
        "compiler_id": compiler_config['name'],
        "compiler_version": compiler_version,  # Add compiler version directly at the top level
        "build_flags_id": build_flags_id,
        "cpu_model": cpu_info,
        "environment": system_info,
        "config": {
            "cmake_build_type": cmake_build_type,
            "cxx_flags_used": cxx_flags,
            "compiler_version": compiler_version,  # Also add to config for backward compatibility
            "toolchain_file": compiler_config['toolchain_file'],
            "gbench_command": f"{experiment['benchmark_executable']} --benchmark_format=json --benchmark_out=..."
        }
    }
    
    # Add experiment-specific configuration if available
    exp_config = get_experiment_config(experiment['name'])
    if exp_config:
        metadata["overrides_applied"] = exp_config
    
    return metadata

def extract_assembly(build_dir, experiment, output_dir):
    """Extract assembly for benchmark functions with source code mapping."""
    logger.info(f"Extracting assembly for {experiment['name']}...")
    
    # Create assembly directory
    assembly_dir = output_dir / "assembly"
    os.makedirs(assembly_dir, exist_ok=True)
    
    # Get the benchmark executable path
    benchmark_exe = build_dir / "experiments" / experiment['name'] / experiment['benchmark_executable']
    
    # First, try to get list of benchmark functions
    try:
        # Run the benchmark with --benchmark_list_tests
        list_cmd = [str(benchmark_exe), "--benchmark_list_tests=true"]
        result = subprocess.run(list_cmd, capture_output=True, text=True, check=True)
        benchmark_functions = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        # If no functions found this way, use default functions based on experiment
        if not benchmark_functions:
            if experiment['name'] == "int_addition":
                benchmark_functions = ["BM_IntAddition"]
            elif experiment['name'] == "float_addition":
                benchmark_functions = ["BM_FloatAddition"]
    except subprocess.SubprocessError:
        # Fallback to default function names
        if experiment['name'] == "int_addition":
            benchmark_functions = ["BM_IntAddition"]
        elif experiment['name'] == "float_addition":
            benchmark_functions = ["BM_FloatAddition"]
        else:
            benchmark_functions = []
    
    if not benchmark_functions:
        logger.warning(f"No benchmark functions found for {experiment['name']}")
        return
    
    # Get source files
    source_files = {}
    source_dir = PROJECT_ROOT / "experiments" / experiment['name'] / "src"
    for source_file in source_dir.glob("**/*.cpp"):
        try:
            with open(source_file, 'r') as f:
                source_files[source_file.name] = f.read()
        except Exception as e:
            logger.warning(f"Could not read source file {source_file}: {e}")
    
    # Platform specific assembly extraction
    is_macos = sys.platform == 'darwin'
    
    if is_macos:
        # macOS specific approach - try llvm-objdump first which handles source better on macOS
        try:
            # Try to use llvm-objdump if available (better support for source+asm on macOS)
            llvm_objdump_cmd = ["llvm-objdump", "-d", "--no-show-raw-insn", "-C", "-S", str(benchmark_exe)]
            result = subprocess.run(llvm_objdump_cmd, capture_output=True, text=True, check=True)
            mixed_assembly = result.stdout
            
            # Write full mixed assembly for reference
            with open(assembly_dir / "full_mixed_assembly.txt", "w") as f:
                f.write(mixed_assembly)
            
            # Extract function-specific mixed assembly 
            for func_name in benchmark_functions:
                lines = mixed_assembly.split('\n')
                capturing = False
                func_mixed_asm = []
                
                for line in lines:
                    if func_name in line and (":" in line or "(" in line):
                        capturing = True
                        func_mixed_asm.append(line)
                    elif capturing:
                        if ("<" in line and ">" in line and ":" in line and not line.strip().startswith(".")) or "}" in line:
                            # Likely a new function or end of function
                            capturing = False
                        else:
                            func_mixed_asm.append(line)
                
                if func_mixed_asm:
                    with open(assembly_dir / f"{func_name}.s", "w") as f:
                        f.write('\n'.join(func_mixed_asm))
                    logger.info(f"Extracted mixed source/assembly for {func_name}")
                else:
                    logger.warning(f"Could not find mixed source/assembly for {func_name}")
        
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Failed to extract with llvm-objdump, trying otool: {e}")
            
            try:
                # Try otool as a fallback on macOS
                otool_cmd = ["otool", "-tV", str(benchmark_exe)]
                result = subprocess.run(otool_cmd, capture_output=True, text=True, check=True)
                disassembly = result.stdout
                
                # Write full disassembly for reference
                with open(assembly_dir / "full_disassembly.txt", "w") as f:
                    f.write(disassembly)
                
                # Extract function-specific assembly and manually integrate source
                for func_name in benchmark_functions:
                    # Look for the function in the disassembly
                    lines = disassembly.split('\n')
                    capturing = False
                    func_asm = []
                    
                    for line in lines:
                        if func_name in line:
                            capturing = True
                            func_asm.append(line)
                        elif capturing:
                            if "_" in line and ":" in line and not any(x in line for x in ["push", "pop", "mov", "add", "sub"]):
                                # Likely a new function
                                capturing = False
                            else:
                                func_asm.append(line)
                    
                    if func_asm:
                        with open(assembly_dir / f"{func_name}.s", "w") as f:
                            # Manually add source code
                            f.write(f"// Source code for {func_name} (manually added):\n")
                            for source_file, content in source_files.items():
                                if func_name in content:
                                    # Extract the function from source (simple approach)
                                    lines = content.split('\n')
                                    func_lines = []
                                    in_func = False
                                    brace_count = 0
                                    
                                    for source_line in lines:
                                        if func_name in source_line and '{' in source_line:
                                            in_func = True
                                            brace_count = 1
                                            func_lines.append(source_line)
                                        elif in_func:
                                            func_lines.append(source_line)
                                            brace_count += source_line.count('{')
                                            brace_count -= source_line.count('}')
                                            if brace_count <= 0:
                                                break
                                    
                                    if func_lines:
                                        f.write('\n'.join(func_lines))
                                        f.write('\n\n')
                            
                            f.write("// Assembly:\n")
                            f.write('\n'.join(func_asm))
                        logger.info(f"Extracted assembly for {func_name} with manually added source")
                    else:
                        logger.warning(f"Could not find assembly for {func_name}")
                
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                logger.warning(f"Failed to extract assembly using otool: {e}")
                # Fall back to extracting source separately
                manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir)
    else:
        # Linux or other platforms - use regular objdump with -S flag
        try:
            # Use objdump to get assembly with source interleaved
            objdump_cmd = ["objdump", "-d", "--no-show-raw-insn", "-C", "-S", str(benchmark_exe)]
            result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True)
            mixed_assembly = result.stdout
            
            # Write full mixed assembly for reference
            with open(assembly_dir / "full_mixed_assembly.txt", "w") as f:
                f.write(mixed_assembly)
            
            # Extract function-specific mixed assembly 
            for func_name in benchmark_functions:
                lines = mixed_assembly.split('\n')
                capturing = False
                func_mixed_asm = []
                
                for line in lines:
                    if func_name in line and ":" in line:
                        capturing = True
                        func_mixed_asm.append(line)
                    elif capturing:
                        if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                            # Likely a new function
                            capturing = False
                        else:
                            func_mixed_asm.append(line)
                
                if func_mixed_asm:
                    with open(assembly_dir / f"{func_name}.s", "w") as f:
                        f.write('\n'.join(func_mixed_asm))
                    logger.info(f"Extracted mixed source/assembly for {func_name}")
                else:
                    logger.warning(f"Could not find mixed source/assembly for {func_name}")
            
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Failed to extract mixed source/assembly, falling back to regular assembly: {e}")
            # Fall back to extracting source separately
            manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir)

def manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir):
    """Fallback function to extract assembly and manually combine with source."""
    try:
        # Fallback to regular objdump without source
        objdump_cmd = ["objdump", "-d", "--no-show-raw-insn", "-C", str(benchmark_exe)]
        result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True)
        disassembly = result.stdout
        
        # Write full disassembly for reference
        with open(assembly_dir / "full_disassembly.txt", "w") as f:
            f.write(disassembly)
        
        # Extract function-specific assembly
        for func_name in benchmark_functions:
            # Look for the function in the disassembly
            lines = disassembly.split('\n')
            capturing = False
            func_asm = []
            
            for line in lines:
                if func_name in line and ":" in line:
                    capturing = True
                    func_asm.append(line)
                elif capturing:
                    if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                        # Likely a new function
                        capturing = False
                    else:
                        func_asm.append(line)
            
            if func_asm:
                with open(assembly_dir / f"{func_name}.s", "w") as f:
                    # Try to manually combine with source for the benchmark function
                    if source_files:
                        f.write(f"// Source code for {func_name} (manually added):\n")
                        for source_file, content in source_files.items():
                            if func_name in content:
                                # Extract the function from source (simple approach)
                                lines = content.split('\n')
                                func_lines = []
                                in_func = False
                                brace_count = 0
                                
                                for source_line in lines:
                                    if func_name in source_line and '{' in source_line:
                                        in_func = True
                                        brace_count = 1
                                        func_lines.append(source_line)
                                    elif in_func:
                                        func_lines.append(source_line)
                                        brace_count += source_line.count('{')
                                        brace_count -= source_line.count('}')
                                        if brace_count <= 0:
                                            break
                                
                                if func_lines:
                                    f.write('\n'.join(func_lines))
                                    f.write('\n\n')
                        
                        f.write("// Assembly:\n")
                    
                    f.write('\n'.join(func_asm))
                logger.info(f"Extracted assembly for {func_name}")
            else:
                logger.warning(f"Could not find assembly for {func_name}")
                
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.warning(f"Failed to extract assembly: {e}")

def run_benchmark(experiment, build_dir, compiler_config, build_flags_id="Release_O3", force=False):
    """Run the benchmark and save results."""
    logger.info(f"Running benchmark for {experiment['name']}...")
    
    # Generate a hash based on metadata
    metadata_hash, metadata_str, detailed_platform_id, detailed_compiler_id = generate_metadata_hash(
        compiler_config['name'], 
        build_flags_id
    )
    
    # Define results directory structure with more detailed paths
    results_base_dir = PROJECT_ROOT / "results" / detailed_platform_id / detailed_compiler_id / build_flags_id / metadata_hash
    results_dir = results_base_dir / experiment['name']
    
    # Check if results already exist
    if results_dir.exists() and not force:
        logger.warning(f"Results for {experiment['name']} already exist at {results_dir}")
        logger.warning(f"Use --force to overwrite existing results.")
        return results_dir
    
    # Create results directory
    os.makedirs(results_dir, exist_ok=True)
    
    # Benchmark executable path
    benchmark_exe = build_dir / "experiments" / experiment['name'] / experiment['benchmark_executable']
    logger.info(f"Looking for benchmark executable at: {benchmark_exe}")
    
    # Results file path for JSON output
    benchmark_output_file = results_dir / "benchmark_output.json"
    
    # Get experiment-specific Google Benchmark arguments
    exp_config = get_experiment_config(experiment['name'])
    gbench_args = []
    if exp_config and "gbench_args" in exp_config:
        gbench_args.extend(exp_config["gbench_args"].split())
    
    # Run the benchmark once to generate JSON output
    json_benchmark_cmd = [
        str(benchmark_exe), 
        "--benchmark_format=json", 
        f"--benchmark_out={benchmark_output_file}"
    ]
    json_benchmark_cmd.extend(gbench_args)
    
    logger.info(f"Running benchmark command: {' '.join(json_benchmark_cmd)}")
    subprocess.run(json_benchmark_cmd, check=True)
    
    # Run perf stat if available (Linux only)
    if platform.system() == "Linux":
        try:
            perf_stat_file = results_dir / "perf_stat.log"
            perf_events = "cycles,instructions,branch-instructions,branch-misses"
            
            # Override perf events if specified in experiment config
            if exp_config and "perf_events" in exp_config:
                perf_events = ",".join(exp_config["perf_events"])
            
            perf_cmd = [
                "perf", "stat", 
                "-o", str(perf_stat_file),
                "-e", perf_events
            ]
            perf_cmd.extend(json_benchmark_cmd)
            
            subprocess.run(perf_cmd, check=True)
            logger.info(f"Performance counters collected with perf")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Failed to run perf: {e}")
    else:
        logger.info(f"Performance counters not collected (perf only available on Linux)")
    
    # Extract assembly
    extract_assembly(build_dir, experiment, results_dir)
    
    # Create and save metadata
    cxx_flags = "-std=c++20"
    cmake_build_type = "Release" if "Release" in build_flags_id else "Debug"
    metadata = create_metadata(
        experiment, 
        compiler_config, 
        build_flags_id, 
        cxx_flags, 
        cmake_build_type, 
        metadata_hash,
        metadata_str,
        detailed_platform_id,
        detailed_compiler_id
    )
    
    with open(results_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Results saved to {results_dir}")
    return results_dir

def main():
    """Main function to run benchmarks and generate reports."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run benchmarks and generate reports')
    parser.add_argument('--config', 
                        help='Path to a custom configuration file')
    parser.add_argument('--compiler', choices=['gcc', 'clang', 'all'], default='all',
                        help='Compiler to use for benchmarks (default: all)')
    parser.add_argument('--experiments', 
                        help='Comma-separated list of experiments to run (default: all)')
    parser.add_argument('--build-flags', default='Release_O3',
                        help='Build flags identifier (e.g., Release_O3, Debug_O0)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-run of benchmarks even if results exist')
    parser.add_argument('--incremental-build', action='store_true',
                        help='Use incremental build instead of clean build')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Filter compilers based on command-line arguments
    compilers = [c for c in config['compilers'] if args.compiler == 'all' or c['name'] == args.compiler]
    
    # Filter experiments based on command-line arguments
    if args.experiments:
        experiment_names = args.experiments.split(',')
        experiments = [e for e in config['experiments'] if e['name'] in experiment_names]
    else:
        experiments = config['experiments']
    
    # Build and run benchmarks for each compiler
    for compiler_config in compilers:
        try:
            # Build with the current compiler
            build_dir, _, _ = build_benchmark(
                compiler_config, 
                build_flags_id=args.build_flags,
                incremental=args.incremental_build
            )
            
            # Run each experiment
            for experiment in experiments:
                results_dir = run_benchmark(
                    experiment, 
                    build_dir, 
                    compiler_config,
                    build_flags_id=args.build_flags,
                    force=args.force
                )
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running benchmark with {compiler_config['name']}: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error with {compiler_config['name']}: {e}")
            continue

if __name__ == "__main__":
    main()