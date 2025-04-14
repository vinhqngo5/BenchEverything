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
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def generate_metadata_hash(compiler_name, build_flags_id, timestamp=None):
    """Generate a hash based on metadata instead of git hash."""
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()
    
    # Concatenate key metadata elements
    metadata_str = f"{platform.system()}-{platform.machine()}:{compiler_name}:{build_flags_id}:{timestamp}"
    
    # Generate a short hash (8 characters)
    hash_obj = hashlib.md5(metadata_str.encode())
    short_hash = hash_obj.hexdigest()[:8]
    
    return short_hash, metadata_str

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
    print(f"Building with {compiler_config['name']}...")
    
    # Get platform identifier
    platform_id = f"{platform.system().lower()}-{platform.machine()}"
    
    # Create build directory with more detailed path
    build_dir = PROJECT_ROOT / "build" / platform_id / compiler_config['name'] / build_flags_id
    
    # Clean build directory if not incremental
    if not incremental and build_dir.exists():
        print(f"Cleaning build directory: {build_dir}")
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
    
    print(f"Running CMake command: {' '.join(cmake_cmd)}")
    subprocess.run(cmake_cmd, check=True)
    
    # Run CMake build
    build_cmd = ["cmake", "--build", str(build_dir), "--parallel"]
    subprocess.run(build_cmd, check=True)
    
    return build_dir, cxx_flags, cmake_build_type

def create_metadata(experiment, compiler_config, build_flags_id, cxx_flags, cmake_build_type, metadata_hash, metadata_str):
    """Create metadata JSON for the experiment run."""
    system_info = get_system_info()
    
    platform_id = f"{platform.system().lower()}-{platform.machine()}"
    timestamp = datetime.datetime.now().isoformat()
    
    metadata = {
        "timestamp_iso": timestamp,
        "metadata_hash": metadata_hash,
        "metadata_source": metadata_str,
        "platform_id": platform_id,
        "compiler_id": compiler_config['name'],
        "build_flags_id": build_flags_id,
        "environment": system_info,
        "config": {
            "cmake_build_type": cmake_build_type,
            "cxx_flags_used": cxx_flags,
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
    """Extract assembly for benchmark functions."""
    print(f"Extracting assembly for {experiment['name']}...")
    
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
        print(f"Warning: No benchmark functions found for {experiment['name']}")
        return
    
    # Disassemble the executable
    try:
        objdump_cmd = ["objdump", "-d", "--no-show-raw-insn", "-C", str(benchmark_exe)]
        result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True)
        disassembly = result.stdout
        
        # Write full disassembly for reference
        with open(assembly_dir / "full_disassembly.txt", "w") as f:
            f.write(disassembly)
        
        # Extract function-specific assembly (simplified approach)
        # In a real implementation, this would need more sophisticated parsing
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
                    f.write('\n'.join(func_asm))
                print(f"Extracted assembly for {func_name}")
            else:
                print(f"Warning: Could not find assembly for {func_name}")
                
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        print(f"Warning: Failed to extract assembly: {e}")

def run_benchmark(experiment, build_dir, compiler_config, build_flags_id="Release_O3", force=False):
    """Run the benchmark and save results."""
    print(f"Running benchmark for {experiment['name']}...")
    
    # Generate a hash based on metadata
    timestamp = datetime.datetime.now().isoformat()
    metadata_hash, metadata_str = generate_metadata_hash(
        compiler_config['name'], 
        build_flags_id,
        timestamp
    )
    
    # Get platform identifier
    platform_id = f"{platform.system().lower()}-{platform.machine()}"
    
    # Define results directory structure following the documented pattern
    # Changed from git hash to metadata hash
    results_base_dir = PROJECT_ROOT / "results" / platform_id / compiler_config['name'] / build_flags_id / metadata_hash
    results_dir = results_base_dir / experiment['name']
    
    # Check if results already exist
    if results_dir.exists() and not force:
        print(f"Results for {experiment['name']} already exist at {results_dir}")
        print(f"Use --force to overwrite existing results.")
        return results_dir
    
    # Create results directory
    os.makedirs(results_dir, exist_ok=True)
    
    # Benchmark executable path
    benchmark_exe = build_dir / "experiments" / experiment['name'] / experiment['benchmark_executable']
    print(f"Looking for benchmark executable at: {benchmark_exe}")
    
    # Results file path
    benchmark_output_file = results_dir / "benchmark_output.json"
    
    # Run the benchmark with Google Benchmark JSON output
    benchmark_cmd = [
        str(benchmark_exe), 
        "--benchmark_format=json", 
        f"--benchmark_out={benchmark_output_file}"
    ]
    
    # Add any experiment-specific Google Benchmark arguments
    exp_config = get_experiment_config(experiment['name'])
    if exp_config and "gbench_args" in exp_config:
        benchmark_cmd.extend(exp_config["gbench_args"].split())
    
    print(f"Running benchmark command: {' '.join(benchmark_cmd)}")
    subprocess.run(benchmark_cmd, check=True)
    
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
            perf_cmd.extend(benchmark_cmd)
            
            subprocess.run(perf_cmd, check=True)
            print(f"Performance counters collected with perf")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"Warning: Failed to run perf: {e}")
    else:
        print(f"Performance counters not collected (perf only available on Linux)")
    
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
        metadata_str
    )
    
    with open(results_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Results saved to {results_dir}")
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
            print(f"Error running benchmark with {compiler_config['name']}: {e}", file=sys.stderr)
            continue
        except Exception as e:
            print(f"Unexpected error with {compiler_config['name']}: {e}", file=sys.stderr)
            continue

if __name__ == "__main__":
    main()