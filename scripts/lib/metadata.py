import hashlib
import datetime
import json
from pathlib import Path
from typing import Dict, Optional, Tuple

from .logger import get_logger
from .environment import (
    get_os, get_arch, get_cpu_model, get_detailed_platform_id, get_platform_id, # <<< ADDED get_platform_id here
    extract_compiler_from_toolchain, get_compiler_version, get_detailed_compiler_id,
    get_full_system_details
)
from .config import BenchEverythingConfig


logger = get_logger()

def generate_metadata_hash(
    detailed_platform_id: str,
    detailed_compiler_id: str,
    build_flags_id: str,
    additional_metadata: Optional[Dict] = None
) -> Tuple[str, str]:
    """
    Generate a hash based on platform, compiler, build flags, and optional additional metadata.

    Returns:
        Tuple of (short_hash, metadata_source_string)
    """
    metadata_components = {
        "platform_id": detailed_platform_id,
        "compiler_id": detailed_compiler_id,
        "build_flags_id": build_flags_id,
    }

    # Add any additional metadata provided
    if additional_metadata:
        # Filter additional_metadata to ensure basic types for hashing consistency
        filtered_additional = {k: str(v) for k, v in additional_metadata.items() if isinstance(v, (str, int, float, bool))}
        metadata_components.update(filtered_additional)

    # Create a sorted representation for consistent hashing
    metadata_items = sorted(metadata_components.items())

    # Create a string representation
    metadata_source_string = "|".join(f"{k}={v}" for k, v in metadata_items)

    # Generate MD5 hash and take the first 8 characters
    hash_obj = hashlib.md5(metadata_source_string.encode('utf-8'))
    short_hash = hash_obj.hexdigest()[:8]

    logger.debug(f"Generated metadata hash '{short_hash}' from source: '{metadata_source_string}'")

    return short_hash, metadata_source_string


def create_metadata_dict(
    config: BenchEverythingConfig,
    experiment_name: str,
    compiler_config: Dict,
    build_flags_id: str,
    cxx_flags_used: str,
    cmake_build_type: str,
    gbench_cmd_base: list # Base command before args specific to this run
) -> Dict:
    """
    Create the complete metadata dictionary for an experiment run.
    """
    project_root = config.get_project_root()

    # --- Gather Environment Info ---
    system_details = get_full_system_details()
    detailed_platform_id = get_detailed_platform_id() # e.g., linux-x86_64-some-cpu

    # --- Gather Compiler Info ---
    toolchain_path_rel = compiler_config.get('toolchain_file', '')
    toolchain_path_abs = project_root / toolchain_path_rel if toolchain_path_rel else None
    compiler_path, compiler_type = extract_compiler_from_toolchain(toolchain_path_abs)
    compiler_version = get_compiler_version(compiler_path)
    detailed_compiler_id = get_detailed_compiler_id(
        compiler_config['name'], compiler_path, compiler_type, compiler_version
    ) # e.g., gcc-11.2.0

    # --- Generate Hash ---
    exp_config = config.load_experiment_config(experiment_name)
    # Include relevant experiment-specific config in the hash if needed
    additional_hash_data = {}
    if exp_config.get("cmake_flags"):
        additional_hash_data["exp_cmake_flags"] = exp_config["cmake_flags"]
    if exp_config.get("cxx_flags"):
        additional_hash_data["exp_cxx_flags"] = exp_config["cxx_flags"]

    metadata_hash, metadata_source_string = generate_metadata_hash(
        detailed_platform_id,
        detailed_compiler_id,
        build_flags_id,
        additional_hash_data
    )

    # --- Construct Final Metadata Dict ---
    timestamp = datetime.datetime.now().isoformat()
    gbench_cmd_str = ' '.join(gbench_cmd_base + [f"--benchmark_out=<results_dir>/benchmark_output.json"])
    if exp_config and "gbench_args" in exp_config:
         gbench_cmd_str += " " + exp_config["gbench_args"]


    metadata = {
        "timestamp_iso": timestamp,
        "experiment_name": experiment_name,
        "metadata_hash": metadata_hash,
        "metadata_source": metadata_source_string,
        "detailed_platform_id": detailed_platform_id,
        "detailed_compiler_id": detailed_compiler_id,
        "platform_id": get_platform_id(), # Simple os-arch <<< FIXED: Was calling undefined function
        "compiler_id": compiler_config['name'], # From global config
        "compiler_type": compiler_type, # Detected type (gcc/clang/etc)
        "compiler_version": compiler_version, # Detected version
        "build_flags_id": build_flags_id,
        "cpu_model": system_details.get('cpu_model', 'unknown'),
        "environment": system_details, # Full system details dict
        "config": {
            "cmake_build_type": cmake_build_type,
            "cxx_flags_used": cxx_flags_used,
            "compiler_path": compiler_path,
            "toolchain_file": toolchain_path_rel,
            "gbench_command_template": gbench_cmd_str, # Example command
        },
        "experiment_config_applied": exp_config if exp_config else {} # Record applied overrides
    }

    return metadata


def save_metadata(metadata_dict: Dict, results_dir: Path):
    """Save the metadata dictionary to metadata.json."""
    output_file = results_dir / "metadata.json"
    try:
        with open(output_file, "w") as f:
            json.dump(metadata_dict, f, indent=2)
        logger.info(f"Metadata saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Failed to save metadata to {output_file}: {e}")
        return False

def load_metadata(results_dir: Path) -> Optional[Dict]:
     """Load metadata from a results directory."""
     metadata_file = results_dir / "metadata.json"
     if not metadata_file.exists():
         logger.warning(f"Metadata file not found: {metadata_file}")
         return None
     try:
         with open(metadata_file, 'r') as f:
             return json.load(f)
     except json.JSONDecodeError as e:
         logger.error(f"Error parsing metadata file {metadata_file}: {e}")
         return None
     except Exception as e:
         logger.error(f"Error loading metadata file {metadata_file}: {e}")
         return None