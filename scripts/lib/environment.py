import platform
import subprocess
import re
import os
from pathlib import Path

from .logger import get_logger

logger = get_logger()

# --- System Information ---

def get_os():
    """Get the operating system name."""
    return platform.system().lower()

def get_arch():
    """Get the machine architecture."""
    return platform.machine()

def get_cpu_model():
    """Get a cleaned CPU model string suitable for paths."""
    cpu_info = "unknown"
    system = get_os()

    if system == "darwin":  # macOS
        try:
            cpu_info = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True, check=False, timeout=5
            ).stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            cpu_info = platform.processor() or "unknown-mac"

    elif system == "linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("model name"):
                        cpu_info = line.split(":", 1)[1].strip()
                        break
                if cpu_info == "unknown": # Fallback if "model name" not found
                     cpu_info = platform.processor() or "unknown-linux"
        except (IOError, FileNotFoundError):
            cpu_info = platform.processor() or "unknown-linux"

    else:  # Windows or other
        cpu_info = platform.processor() or "unknown"

    # Clean up and normalize
    cpu_info = " ".join(cpu_info.split())
    cpu_info = re.sub(r'\s+@\s+\d+\.\d+GHz', '', cpu_info)
    cpu_info = cpu_info.replace("Intel(R) Core(TM) ", "")
    cpu_info = cpu_info.replace("AMD ", "")
    cpu_info = re.sub(r'[^a-zA-Z0-9-]', '-', cpu_info)
    cpu_info = re.sub(r'-+', '-', cpu_info)
    cpu_info = cpu_info.strip('-')

    # Limit length for path safety
    max_len = 40
    if len(cpu_info) > max_len:
        cpu_info = cpu_info[:max_len]

    return cpu_info if cpu_info else "unknown-cpu"


def get_platform_id():
    """Get a simple platform identifier (e.g., 'linux-x86_64')."""
    return f"{get_os()}-{get_arch()}"

def get_detailed_platform_id():
    """Get a more detailed platform identifier including CPU model."""
    return f"{get_os()}-{get_arch()}-{get_cpu_model()}"

def get_full_system_details():
    """Get a dictionary with detailed system information."""
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(), # Raw processor info
        "cpu_model": get_cpu_model(), # Cleaned CPU model
        "python_version": platform.python_version(),
    }

    # Add common compiler versions if available in PATH
    for compiler_cmd, key in [("g++", "gcc_path_version"), ("clang++", "clang_path_version")]:
        try:
            result = subprocess.run([compiler_cmd, "--version"], capture_output=True, text=True, check=False, timeout=5)
            if result.returncode == 0:
                system_info[key] = result.stdout.strip().split('\n')[0]
            else:
                 system_info[key] = "Not available or error"
        except FileNotFoundError:
            system_info[key] = "Not found in PATH"
        except subprocess.TimeoutExpired:
            system_info[key] = "Timeout executing --version"
        except Exception as e:
             system_info[key] = f"Error getting version: {e}"


    return system_info


# --- Compiler Information ---

def extract_compiler_from_toolchain(toolchain_file_path):
    """Extract the C++ compiler path and type ('gcc', 'clang', or 'unknown') from a toolchain file."""
    compiler_path_str = None
    compiler_type = 'unknown'
    toolchain_path = Path(toolchain_file_path)

    if not toolchain_path.exists():
        logger.warning(f"Toolchain file not found: {toolchain_path}")
        return None, compiler_type

    try:
        with open(toolchain_path, 'r') as f:
            content = f.read()

        # Look for CMAKE_CXX_COMPILER definition
        match = re.search(r'set\s*\(\s*CMAKE_CXX_COMPILER\s+["\']?([^)\s"\']+)["\']?\s*\)', content, re.IGNORECASE)
        if match:
            compiler_path_str = match.group(1).strip()
            compiler_path = Path(compiler_path_str)

            # Determine type based on executable name
            exe_name = compiler_path.name.lower()
            if "clang++" in exe_name or "clang" in exe_name:
                compiler_type = "clang"
            elif "g++" in exe_name or "gcc" in exe_name:
                compiler_type = "gcc"
            elif "cl.exe" in exe_name or "msvc" in exe_name:
                 compiler_type = "msvc" # Basic MSVC detection

            # Make path absolute if it's relative within the toolchain file context (tricky)
            # For simplicity, we assume toolchain paths are absolute or resolvable from project root
            # If the path isn't absolute, try resolving relative to project root
            if not compiler_path.is_absolute():
                 # This assumes the toolchain file path itself is relative to project root or absolute
                 project_root = toolchain_path.parent.parent.parent # Heuristic: assumes cmake/toolchains/
                 resolved_path = (project_root / compiler_path_str).resolve()
                 if resolved_path.exists():
                      compiler_path_str = str(resolved_path)
                 else:
                      # Maybe it's in PATH? Or relative to build dir? Hard to tell without context.
                      logger.debug(f"Could not resolve relative compiler path '{compiler_path_str}' found in toolchain.")
                      # Keep the original string, maybe it's in PATH
                      pass

            logger.debug(f"Found compiler path: {compiler_path_str}, type: {compiler_type}")
            return compiler_path_str, compiler_type
        else:
            logger.warning(f"CMAKE_CXX_COMPILER definition not found in {toolchain_path}")
            return None, compiler_type
    except Exception as e:
        logger.warning(f"Error extracting compiler from toolchain file {toolchain_path}: {e}")
        return None, compiler_type


def get_compiler_version(compiler_path_str):
    """Get the compiler version by running the executable."""
    version = "unknown"
    if not compiler_path_str:
        return version

    try:
        # Try common version flags
        for flag in ["--version", "-dumpversion"]:
            cmd = [compiler_path_str, flag]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=False, timeout=5
            )

            if result.returncode == 0 and result.stdout:
                # Try to extract semantic version first (most reliable)
                version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
                if version_match:
                    version = version_match.group(1)
                    logger.debug(f"Extracted version {version} using flag {flag} for {compiler_path_str}")
                    return version

                # Try to extract simpler version (e.g., just major for -dumpversion)
                version_match_simple = re.search(r'(\d+\.\d+)', result.stdout)
                if version_match_simple:
                     version = version_match_simple.group(1)
                     logger.debug(f"Extracted version {version} using flag {flag} for {compiler_path_str}")
                     return version

                # Fallback: Use the first line, cleaned
                first_line = result.stdout.split('\n')[0].strip()
                # Remove extra info often added by compilers
                first_line = re.sub(r'\s*\(.*\)\s*', '', first_line).strip()
                # Basic cleaning for path safety
                cleaned_version = re.sub(r'[^a-zA-Z0-9\._-]', '-', first_line)
                if cleaned_version:
                    version = cleaned_version
                    logger.debug(f"Extracted version '{version}' using flag {flag} for {compiler_path_str} (fallback)")
                    return version # Return as soon as we get *something* valid

    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Could not determine version for compiler at {compiler_path_str}: {e}")
    except Exception as e: # Catch potential regex errors or others
         logger.warning(f"Unexpected error getting version for {compiler_path_str}: {e}")


    if version == "unknown":
        logger.warning(f"Failed to determine version for compiler: {compiler_path_str}")

    return version


def get_detailed_compiler_id(compiler_config_name, compiler_path, compiler_type, compiler_version):
    """Get a detailed compiler identifier including version (e.g., 'gcc-11.2.0')."""
    # Prefer the detected type (gcc/clang) if available, otherwise use the name from config
    base_name = compiler_type if compiler_type not in [None, 'unknown'] else compiler_config_name
    version = compiler_version if compiler_version != "unknown" else "unknown_version"

    # Sanitize base_name just in case
    base_name = re.sub(r'[^a-zA-Z0-9-]', '-', base_name)

    return f"{base_name}-{version}"