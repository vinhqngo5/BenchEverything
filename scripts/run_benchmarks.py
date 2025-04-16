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

def get_compiler_version(compiler_path):
    """Get the compiler version by running the actual compiler executable.
    
    Args:
        compiler_path: The path to the compiler executable from the toolchain file
        
    Returns:
        The version string, or "unknown" if it can't be determined
    """
    version = "unknown"
    
    try:
        # Run the compiler with --version flag
        result = subprocess.run(
            [compiler_path, "--version"],
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
                # Clean up version for path use
                version = re.sub(r'[^a-zA-Z0-9\.-]', '-', version)
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.warning(f"Could not determine version for compiler at {compiler_path}: {e}")
    
    return version

def generate_metadata_hash(compiler_config, build_flags_id, additional_metadata=None):
    """Generate a hash based on metadata.
    
    Args:
        compiler_config: The compiler configuration dictionary
        build_flags_id: Build flags identifier (e.g., 'Release_O3')
        additional_metadata: Optional dictionary containing additional metadata to include in the hash
        
    Returns:
        Tuple of (short_hash, metadata_str, detailed_platform_id, detailed_compiler_id)
    """
    # Get system information
    system = platform.system().lower()
    machine = platform.machine()
    cpu = get_cpu_info()
    
    # Extract the actual compiler path and type from the toolchain file
    toolchain_path = os.path.join(PROJECT_ROOT, compiler_config['toolchain_file'])
    compiler_path, compiler_type = extract_compiler_from_toolchain(toolchain_path)
    
    # Get compiler version using the actual compiler path
    if compiler_path:
        compiler_version = get_compiler_version(compiler_path)
    else:
        logger.warning(f"Could not extract compiler path from {toolchain_path}, using default version")
        compiler_version = "unknown"
    
    # Use the canonical compiler type (gcc/clang) if available, otherwise use the name from config
    canonical_compiler_name = compiler_type if compiler_type else compiler_config['name']
    
    # Create metadata dictionary with standard fields
    metadata = {
        "system": system,
        "machine": machine,
        "cpu": cpu,
        "compiler_name": compiler_config['name'],
        "compiler_type": canonical_compiler_name,
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
    
    # Create a compiler id that includes version - use canonical name where possible
    detailed_compiler_id = f"{canonical_compiler_name}-{compiler_version}"
    
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
        compiler_config, 
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
    if "RelWithDebInfo" in build_flags_id:
        cmake_build_type = "RelWithDebInfo"
    elif "Release" in build_flags_id:
        cmake_build_type = "Release"
    elif "Debug" in build_flags_id:
        cmake_build_type = "Debug"
    else:
        cmake_build_type = "Release"  # Default to Release
    
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
    
    # Extract the actual compiler path and type from the toolchain file
    toolchain_path = os.path.join(PROJECT_ROOT, compiler_config['toolchain_file'])
    compiler_path, compiler_type = extract_compiler_from_toolchain(toolchain_path)
    
    # Get compiler version using the actual compiler path
    if compiler_path:
        compiler_version = get_compiler_version(compiler_path)
    else:
        logger.warning(f"Could not extract compiler path from {toolchain_path}, using unknown version")
        compiler_version = "unknown"
    
    timestamp = datetime.datetime.now().isoformat()
    
    metadata = {
        "timestamp_iso": timestamp,
        "metadata_hash": metadata_hash,
        "metadata_source": metadata_str,
        "detailed_platform_id": detailed_platform_id,
        "detailed_compiler_id": detailed_compiler_id,
        "platform_id": f"{platform.system().lower()}-{platform.machine()}",
        "compiler_id": compiler_config['name'],
        "compiler_version": compiler_version,
        "build_flags_id": build_flags_id,
        "cpu_model": cpu_info,
        "environment": system_info,
        "config": {
            "cmake_build_type": cmake_build_type,
            "cxx_flags_used": cxx_flags,
            "compiler_version": compiler_version,
            "compiler_path": compiler_path,
            "compiler_type": compiler_type,
            "toolchain_file": compiler_config['toolchain_file'],
            "gbench_command": f"{experiment['benchmark_executable']} --benchmark_format=json --benchmark_out=..."
        }
    }
    
    # Add experiment-specific configuration if available
    exp_config = get_experiment_config(experiment['name'])
    if exp_config:
        metadata["overrides_applied"] = exp_config
    
    return metadata

def _get_benchmark_functions_nm_mapping(benchmark_exe):
    """Get a mapping from benchmark function names to their mangled names using nm."""
    try:
        # Run nm with demangling to get symbol information
        nm_cmd = ["nm", "-C", str(benchmark_exe)]
        result = subprocess.run(nm_cmd, capture_output=True, text=True, check=True)
        
        # Parse the output to find benchmark functions
        benchmark_functions = []
        name_mapping = {}  # Maps benchmark names to their fully mangled versions
        
        for line in result.stdout.splitlines():
            if "BM_" in line:  # Only look at benchmark functions
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    demangled_name = parts[2]
                    # Extract just the function name part for our benchmark functions
                    if demangled_name.startswith("void BM_"):
                        # Remove the "void " prefix and anything after the function signature
                        func_sig = demangled_name.split("(")[0][5:]  # Remove "void " and anything after "("
                        
                        # Simplify the name for matching purposes (converts from mangled to clean name)
                        clean_name = func_sig
                        # Replace std::__1:: with std::
                        clean_name = clean_name.replace("std::__1::", "std::")
                        # Remove allocator references
                        clean_name = re.sub(r', std::\w+<[^>]+>\s*>', '>', clean_name)
                        
                        # Add to the list of benchmark functions
                        benchmark_functions.append(clean_name)
                        # Save mapping between clean name and demangled name
                        name_mapping[clean_name] = func_sig
        
        return benchmark_functions, name_mapping
    except Exception as e:
        logger.warning(f"Error getting function names using nm: {e}")
        return [], {}

def extract_assembly(build_dir, experiment, output_dir, build_flags_id="Release_O3"):
    """Extract assembly for benchmark functions with source code mapping."""
    logger.info(f"Extracting assembly for {experiment['name']}...")
    
    # Create assembly directory
    assembly_dir = output_dir / "assembly"
    os.makedirs(assembly_dir, exist_ok=True)
    
    # Get the benchmark executable path
    benchmark_exe = build_dir / "experiments" / experiment['name'] / experiment['benchmark_executable']
    
    # First, try to get list of benchmark functions
    # Try to get benchmark functions from nm first (more reliable)
    benchmark_functions, name_mapping = _get_benchmark_functions_nm_mapping(benchmark_exe)
    
    # If that fails, fall back to the original method
    if not benchmark_functions:
        logger.info("Could not get benchmark functions from nm, falling back to --benchmark_list_tests")
        benchmark_functions = _get_benchmark_functions(benchmark_exe, experiment)
    
    if not benchmark_functions:
        logger.warning(f"No benchmark functions found for {experiment['name']}")
        return
    
    # Get source files
    source_files = _get_source_files(experiment)
    
    # Check build type
    is_macos = platform.system() == 'Darwin'
    has_debug_info = "Debug" in build_flags_id or "RelWithDebInfo" in build_flags_id
    
    try:
        if has_debug_info:
            # Try to extract assembly with source interleaving for builds with debug info
            if is_macos:
                # For macOS Debug or RelWithDebInfo builds, run dsymutil first
                _run_dsymutil(benchmark_exe)
            
            # Try to extract assembly with objdump and debug info
            success = _extract_with_objdump(benchmark_exe, benchmark_functions, assembly_dir, has_debug_info, name_mapping)
            
            if not success:
                logger.info("Objdump extraction with debug info failed, falling back to manual extraction")
                manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)
        else:
            # For Release builds without debug info, use manual extraction
            logger.info("Release build without debug info, using manual assembly extraction")
            manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)
            
    except Exception as e:
        logger.warning(f"Error extracting assembly: {e}")
        # Fall back to manual extraction as last resort
        logger.info("Using manual assembly extraction as fallback")
        manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)

def _get_benchmark_functions(benchmark_exe, experiment):
    """Get list of benchmark functions."""
    try:
        # Run the benchmark with --benchmark_list_tests
        list_cmd = [str(benchmark_exe), "--benchmark_list_tests=true"]
        result = subprocess.run(list_cmd, capture_output=True, text=True, check=True)
        benchmark_functions = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        # If no functions found this way, use default functions based on experiment
        if not benchmark_functions:
            benchmark_functions = _get_default_benchmark_functions(experiment)
        return benchmark_functions
    except subprocess.SubprocessError:
        # Fallback to default function names
        return _get_default_benchmark_functions(experiment)

def _get_default_benchmark_functions(experiment):
    """Get default benchmark function names based on experiment type."""
    # if experiment['name'] == "int_addition":
    #     return ["BM_IntAddition"]
    # elif experiment['name'] == "float_addition":
    #     return ["BM_FloatAddition"]
    # else:
    return []

def _get_source_files(experiment):
    """Get source files for the experiment."""
    source_files = {}
    source_dir = PROJECT_ROOT / "experiments" / experiment['name'] / "src"
    for source_file in source_dir.glob("**/*.cpp"):
        try:
            with open(source_file, 'r') as f:
                source_files[source_file.name] = f.read()
        except Exception as e:
            logger.warning(f"Could not read source file {source_file}: {e}")
    return source_files

def _run_dsymutil(benchmark_exe):
    """Run dsymutil to generate debug symbols (macOS specific)."""
    try:
        logger.info(f"Running dsymutil to generate debug symbols for {benchmark_exe}")
        dsymutil_cmd = ["dsymutil", str(benchmark_exe)]
        subprocess.run(dsymutil_cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        logger.warning(f"Failed to run dsymutil: {e}")
        return False

def _extract_with_objdump(benchmark_exe, benchmark_functions, assembly_dir, has_debug_info, name_mapping=None):
    """Extract assembly using objdump with appropriate flags."""
    try:
        # Build objdump command with appropriate flags
        objdump_flags = ["-d", "--no-show-raw-insn", "-C"]
        if has_debug_info:
            objdump_flags.insert(0, "-S")  # Add source only if debug info is available
            
        objdump_cmd = ["objdump"] + objdump_flags + [str(benchmark_exe)]
        logger.info(f"Running: {' '.join(objdump_cmd)}")
        
        result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True)
        mixed_assembly = result.stdout
        
        # Write full mixed assembly for reference
        with open(assembly_dir / "full_mixed_assembly.txt", "w") as f:
            f.write(mixed_assembly)
        
        # Extract function-specific assembly
        for func_name in benchmark_functions:
            # If we have name mapping from nm, use it for more precise matching
            lookup_name = name_mapping.get(func_name, func_name) if name_mapping else func_name
            
            func_asm = _extract_function_assembly(mixed_assembly, lookup_name, func_name)
            
            if func_asm:
                with open(assembly_dir / f"{func_name}.s", "w") as f:
                    f.write("\n".join(func_asm))
                logger.info(f"Extracted {'mixed source/' if has_debug_info else ''}assembly for {func_name}")
            else:
                logger.warning(f"Could not find {func_name} in assembly output")
                
        return True
    except Exception as e:
        logger.warning(f"Error extracting assembly with objdump: {e}")
        return False

def _extract_function_assembly(assembly_text, lookup_name, original_name=None):
    """Extract assembly for a specific function from full assembly text.
    
    Args:
        assembly_text: The full assembly text to search
        lookup_name: The actual name to look for in the assembly (possibly mangled)
        original_name: The original benchmark name (for comments)
    """
    lines = assembly_text.splitlines()
    func_asm = []
    capturing = False
    
    # Use the original name for comments if provided
    comment_name = original_name if original_name else lookup_name
    
    # Try direct match first
    for i, line in enumerate(lines):
        # Look for function start marker
        if lookup_name in line and ":" in line:
            capturing = True
            # Add a comment with the original benchmark name if it's different
            if original_name and lookup_name != original_name:
                func_asm.append(f"// Assembly for benchmark function: {original_name}")
            func_asm.append(line)
        elif capturing:
            # Look for function end marker (next function or end of file)
            if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                capturing = False
            else:
                func_asm.append(line)
    
    # If we didn't find a match but have a template function, try a more flexible approach
    if not func_asm and "<" in lookup_name and ">" in lookup_name:
        # Get the base name (before the template part)
        base_name = lookup_name.split("<")[0]
        
        for i, line in enumerate(lines):
            if base_name in line and "<" in line and ">" in line and ":" in line:
                # Make sure this is the right function by checking parts of the template
                template_parts = re.findall(r'<([^<>]+)>', lookup_name)
                if template_parts and all(part in line for part in template_parts):
                    capturing = True
                    # Add a comment with the original benchmark name
                    if original_name:
                        func_asm.append(f"// Assembly for benchmark function: {original_name}")
                    func_asm.append(line)
            elif capturing:
                if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                    capturing = False
                else:
                    func_asm.append(line)
    
    return func_asm

def manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping=None):
    """Fallback function to extract assembly and manually combine with source."""
    try:
        # Try with standard objdump to get full disassembly
        objdump_cmd = ["objdump", "-d", "--no-show-raw-insn", "-C", str(benchmark_exe)]
        result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True)
        disassembly = result.stdout
        
        # Write full disassembly for reference
        with open(assembly_dir / "full_disassembly.txt", "w") as f:
            f.write(disassembly)
        
        # Extract function-specific assembly using nm name mapping if available
        lines = disassembly.split('\n')
        
        for func_name in benchmark_functions:
            # If we have a name mapping from nm, use the mapped name for lookup
            lookup_name = name_mapping.get(func_name, func_name) if name_mapping else func_name
            
            # For template functions, get the base name for template extraction
            is_template = '<' in func_name
            base_name = func_name.split('<')[0] if is_template else func_name
            
            # Try with the mapped name from nm first
            func_asm = _extract_direct_match(lines, lookup_name, func_name)
            
            # If that fails and we don't have a mapping or the mapping didn't help,
            # fall back to our multi-strategy approach
            if not func_asm and (not name_mapping or lookup_name == func_name):
                # Strategy 2: Regex pattern match for C++ templates
                func_asm = _extract_template_match(lines, func_name)
                
                # Strategy 3: Base name match
                if not func_asm:
                    func_asm = _extract_base_name_match(lines, func_name)
                
                # Strategy 4: Generic pattern match (most relaxed)
                if not func_asm:
                    func_asm = _extract_generic_match(lines, func_name)
            
            # Create the assembly file
            with open(assembly_dir / f"{func_name}.s", "w") as f:
                # If it's a template function, extract the template definition first
                if is_template:
                    template_def = extract_template_definition(source_files, base_name)
                    if template_def:
                        f.write(f"// Template definition for {base_name}:\n")
                        f.write(template_def)
                        f.write("\n\n")
                    else:
                        f.write(f"// Could not find template definition for {base_name}\n\n")
                
                # Include any assembly we found
                if func_asm:
                    f.write("// Assembly:\n")
                    f.write('\n'.join(func_asm))
                    logger.info(f"Extracted assembly for {func_name}")
                else:
                    f.write(f"// Note: Assembly for {func_name} could not be found\n")
                    f.write(f"// Look for function containing '{base_name}' in full_disassembly.txt\n")
                    logger.warning(f"Could not find assembly for {func_name}")
                
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.warning(f"Failed to extract assembly: {e}")

def _extract_direct_match(lines, lookup_name, original_name=None):
    """Extract assembly using direct string match."""
    func_asm = []
    capturing = False
    
    # Use the original name for comments if provided
    comment_name = original_name if original_name else lookup_name
    
    for line in lines:
        if lookup_name in line and ":" in line:
            capturing = True
            # Add a comment with the original benchmark name if it's different
            if original_name and lookup_name != original_name:
                func_asm.append(f"// Assembly for benchmark function: {comment_name}")
            func_asm.append(line)
        elif capturing:
            if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                capturing = False
            else:
                func_asm.append(line)
    
    return func_asm

def _extract_template_match(lines, func_name):
    """Extract assembly using regex matching for C++ templates."""
    func_asm = []
    capturing = False
    
    # Extract base name and template part
    match = re.match(r'([^<]+)(<.*>)?', func_name)
    if not match:
        return []
        
    base_name, template_part = match.groups()
    
    # Create regex pattern for mangled name
    if template_part:
        # Remove spaces for better matching
        clean_template = template_part.replace(" ", "")
        
        # Replace std:: with std::(__1::)? to handle libc++ mangling
        template_regex = clean_template.replace('std::', r'std::(?:__1::)?')
        
        # Handle additional template parameters that might be added
        template_regex = re.sub(r'>$', r'(?:,std::(?:__1::)?allocator<[^>]+>)?>)', template_regex)
        
        # Make the pattern more flexible by allowing extra characters
        pattern = re.compile(re.escape(base_name) + r'<.*' + 
                            re.escape(clean_template.split('<')[1].split('>')[0].split(',')[0]) + 
                            r'.*>')
    else:
        pattern = re.compile(re.escape(base_name) + r'(?:<.*>)?')
    
    # Try to find the function with the regex pattern
    for line in lines:
        if "<" in line and ">" in line and ":" in line and pattern.search(line):
            capturing = True
            func_asm.append(f"// Best-effort match for {func_name} using pattern matching:\n{line}")
        elif capturing:
            if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                capturing = False
            else:
                func_asm.append(line)
    
    return func_asm

def _extract_base_name_match(lines, func_name):
    """Extract assembly using just the base name of the function."""
    func_asm = []
    capturing = False
    
    # Get base name without any templates
    base_name = func_name.split('<')[0] if '<' in func_name else func_name
    
    for line in lines:
        if base_name in line and "<" in line and ">" in line and ":" in line:
            capturing = True
            func_asm.append(f"// Possible match for {func_name} using base name {base_name}:\n{line}")
        elif capturing:
            if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                capturing = False
            else:
                func_asm.append(line)
    
    return func_asm

def _extract_generic_match(lines, func_name):
    """Generic pattern matching as a last resort."""
    func_asm = []
    capturing = False
    
    # For templated functions, extract the template arguments to look for
    template_args = []
    if '<' in func_name and '>' in func_name:
        template_part = func_name[func_name.find('<')+1:func_name.rfind('>')]
        # Extract container types and values for matching
        template_args = re.findall(r'std::(\w+)|(\d+)', template_part)
        template_args = [x[0] or x[1] for x in template_args if x[0] or x[1]]
    
    # If we have template args, look for lines containing both the base function name and the args
    if template_args:
        base_name = func_name.split('<')[0]
        for line in lines:
            if base_name in line and all(arg in line for arg in template_args) and "<" in line and ":" in line:
                capturing = True
                func_asm.append(f"// Best-effort match for {func_name} using pattern matching:\n{line}")
            elif capturing:
                if "<" in line and ">" in line and ":" in line and not line.strip().startswith("."):
                    capturing = False
                else:
                    func_asm.append(line)
    
    return func_asm

def extract_template_definition(source_files, base_func_name):
    """Extract the template definition for a benchmark function.
    
    Args:
        source_files: Dict mapping filenames to content
        base_func_name: The base function name without template parameters
        
    Returns:
        The template definition as a string, or None if not found
    """
    for source_file, content in source_files.items():
        # Look for the template definition
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Check for template definition patterns
            if "template" in line and "<" in line and ">" in line:
                # Check if the next lines contain the function name
                for j in range(i+1, min(i+5, len(lines))):
                    if j < len(lines) and base_func_name in lines[j]:
                        # Found the function, now extract the complete definition
                        start_line = i
                        func_lines = []
                        brace_count = 0
                        in_function = False
                        
                        # Include the template line
                        func_lines.append(lines[start_line])
                        
                        # Continue until we find the function opening brace
                        k = start_line + 1
                        while k < len(lines) and not in_function:
                            func_lines.append(lines[k])
                            if "{" in lines[k]:
                                in_function = True
                                brace_count = lines[k].count('{')
                            k += 1
                        
                        # Continue until the function is complete (all braces matched)
                        while k < len(lines) and in_function:
                            line = lines[k]
                            func_lines.append(line)
                            brace_count += line.count('{')
                            brace_count -= line.count('}')
                            if brace_count <= 0:
                                break
                            k += 1
                        
                        return '\n'.join(func_lines)
            
            # Also check for static template function definitions without "template" on the same line
            elif base_func_name in line and "<" in line and ">" in line and ("{" in line or ";" in line):
                # Look backwards for the template definition
                for j in range(i-1, max(0, i-5), -1):
                    if "template" in lines[j] and "<" in lines[j] and ">" in lines[j]:
                        # Found the template declaration, now extract the complete definition
                        start_line = j
                        func_lines = []
                        brace_count = 0
                        in_function = False
                        
                        # Include lines from template declaration to function definition
                        for l in range(start_line, i+1):
                            func_lines.append(lines[l])
                            if "{" in lines[l]:
                                in_function = True
                                brace_count = lines[l].count('{')
                        
                        # If the function has a body, extract it
                        if in_function:
                            k = i + 1
                            while k < len(lines) and brace_count > 0:
                                line = lines[k]
                                func_lines.append(line)
                                brace_count += line.count('{')
                                brace_count -= line.count('}')
                                k += 1
                            
                            return '\n'.join(func_lines)
        
    return None

def run_benchmark(experiment, build_dir, compiler_config, build_flags_id="Release_O3", force=False):
    """Run the benchmark and save results."""
    logger.info(f"Running benchmark for {experiment['name']}...")
    
    # Generate a hash based on metadata
    metadata_hash, metadata_str, detailed_platform_id, detailed_compiler_id = generate_metadata_hash(
        compiler_config, 
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
    extract_assembly(build_dir, experiment, results_dir, build_flags_id)
    
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

def extract_compiler_from_toolchain(toolchain_file_path):
    """Extract the actual compiler path and type from a toolchain file.
    
    Args:
        toolchain_file_path: Path to the toolchain file
        
    Returns:
        Tuple of (compiler_path, compiler_type) where compiler_type is 'gcc', 'clang', or None
    """
    try:
        with open(toolchain_file_path, 'r') as f:
            content = f.read()
            
        # Look for the C++ compiler definition
        match = re.search(r'set\(CMAKE_CXX_COMPILER\s+([^\)]+)\)', content)
        if match:
            compiler_path = match.group(1).strip()
            # Remove quoted strings if present
            compiler_path = compiler_path.strip('"\'')
            
            # Determine the compiler type based on the path or name
            compiler_type = None
            if "g++" in compiler_path:
                compiler_type = "gcc"
            elif "clang++" in compiler_path:
                compiler_type = "clang"
                
            return compiler_path, compiler_type
        else:
            logger.warning(f"No C++ compiler definition found in {toolchain_file_path}")
            return None, None
    except Exception as e:
        logger.warning(f"Error extracting compiler from toolchain file {toolchain_file_path}: {e}")
        return None, None

def main():
    """Main function to run benchmarks and generate reports."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run benchmarks and generate reports')
    parser.add_argument('--config', 
                        help='Path to a custom configuration file (default: benchmark_config.json)')
    parser.add_argument('--compiler', 
                        help='Comma-separated list of compilers to use (default: all)')
    parser.add_argument('--experiments', 
                        help='Comma-separated list of experiments to run (default: all)')
    parser.add_argument('--build-flags', default='Release_O3',
                        help='Build flags identifier (e.g., Release_O3, Debug_O0, RelWithDebInfo_O3)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-run of benchmarks even if results exist')
    parser.add_argument('--incremental-build', action='store_true',
                        help='Use incremental build instead of clean build')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Filter compilers based on command-line arguments
    compilers = []
    if args.compiler:
        # Parse comma-separated list of compiler names
        requested_compilers = args.compiler.split(',')
        
        # For each compiler in config, extract its actual compiler type from toolchain
        for compiler_config in config['compilers']:
            # Extract the actual compiler path and type from the toolchain file
            toolchain_path = os.path.join(PROJECT_ROOT, compiler_config['toolchain_file'])
            compiler_path, compiler_type = extract_compiler_from_toolchain(toolchain_path)
            
            # If config name is in the requested list, use it
            if compiler_config['name'] in requested_compilers:
                compilers.append(compiler_config)
                logger.info(f"Using compiler: {compiler_config['name']} (path: {compiler_path}, type: {compiler_type})")
            # Or if compiler type matches a requested compiler
            elif compiler_type and compiler_type in requested_compilers:
                compilers.append(compiler_config)
                logger.info(f"Using compiler: {compiler_config['name']} (identified as {compiler_type})")
    else:
        # Use all compilers if none specified
        compilers = config['compilers']
        
    if not compilers:
        logger.warning(f"No matching compilers found for: {args.compiler}")
        return
    
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