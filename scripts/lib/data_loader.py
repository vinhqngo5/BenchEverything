import json
import glob
from pathlib import Path
from typing import Optional, Dict, List, Tuple

from .logger import get_logger

logger = get_logger()

def validate_path(path) -> Optional[Path]:
    """Validate that a path exists and return a Path object."""
    path_obj = Path(path)
    if not path_obj.exists():
        logger.error(f"Path does not exist: {path}")
        return None
    return path_obj

def load_gbench_json(file_path: Path) -> Optional[Dict]:
    """Load and parse benchmark_output.json."""
    if not file_path.exists():
        logger.warning(f"Google Benchmark JSON file not found: {file_path}")
        return None
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing Google Benchmark JSON {file_path}: {e}")
        return None
    except Exception as e:
         logger.error(f"Error reading file {file_path}: {e}")
         return None


def load_metadata_json(file_path: Path) -> Optional[Dict]:
    """Load and parse metadata.json."""
    if not file_path.exists():
        logger.warning(f"Metadata file not found: {file_path}")
        return None
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing metadata JSON {file_path}: {e}")
        return None
    except Exception as e:
         logger.error(f"Error reading file {file_path}: {e}")
         return None

def load_perf_log(file_path: Path) -> Optional[str]:
    """Read content from perf_stat.log."""
    if not file_path.exists():
        logger.debug(f"Perf log file not found: {file_path}")
        return None # Not an error if perf wasn't run
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading perf log {file_path}: {e}")
        return None

def find_assembly_files(assembly_dir: Path) -> Dict[str, Path]:
    """Find assembly files (.s) in the assembly directory."""
    assembly_files = {}
    if not assembly_dir.is_dir():
        logger.debug(f"Assembly directory not found or not a directory: {assembly_dir}")
        return {}

    for asm_file in assembly_dir.glob("*.s"):
        func_name = asm_file.stem # Use filename without extension as function name key
        assembly_files[func_name] = asm_file # Store the Path object

    # Log markers for failures if they exist
    if (assembly_dir / "_no_functions_found.txt").exists():
         logger.warning(f"Assembly extraction skipped for this run (no functions found): {assembly_dir}")
    if (assembly_dir / "_extraction_failed.txt").exists():
         logger.warning(f"Assembly extraction failed for this run: {assembly_dir}")
    if (assembly_dir / "_extraction_error.txt").exists():
         logger.error(f"Assembly extraction encountered an error for this run: {assembly_dir}")

    return assembly_files

class BenchmarkRunData:
     """Holds loaded data for a single benchmark run."""
     def __init__(self, results_dir: Path):
          self.results_dir = results_dir
          self.gbench_data: Optional[Dict] = None
          self.metadata: Optional[Dict] = None
          self.perf_log: Optional[str] = None
          self.assembly_files: Dict[str, Path] = {} # Map func name to Path
          self.load_error = False

     def load(self):
          logger.debug(f"Loading data from: {self.results_dir}")
          self.gbench_data = load_gbench_json(self.results_dir / "benchmark_output.json")
          self.metadata = load_metadata_json(self.results_dir / "metadata.json")
          self.perf_log = load_perf_log(self.results_dir / "perf_stat.log")
          self.assembly_files = find_assembly_files(self.results_dir / "assembly")

          # Basic check for essential data
          if self.gbench_data is None or self.metadata is None:
               logger.warning(f"Essential data (gbench/metadata) missing for run: {self.results_dir}")
               self.load_error = True
          return not self.load_error

def load_benchmark_run(results_dir_path: Path) -> Optional[BenchmarkRunData]:
    """Load all data for a single benchmark run into a BenchmarkRunData object."""
    if not results_dir_path or not results_dir_path.is_dir():
        logger.error(f"Invalid results directory path provided: {results_dir_path}")
        return None

    run_data = BenchmarkRunData(results_dir_path)
    if run_data.load():
        return run_data
    else:
        return None # Indicate loading failed

def find_all_result_dirs(project_root: Path) -> List[Path]:
    """Find all valid experiment result directories under results/."""
    results_root = project_root / "results"
    if not results_root.is_dir():
        logger.warning(f"Base results directory not found: {results_root}")
        return []

    # Pattern: results/*/*/*/*/<experiment_name>
    # Where the '*' represent platform, compiler, flags, hash
    pattern = str(results_root / "*" / "*" / "*" / "*" / "*")
    potential_dirs = glob.glob(pattern)

    valid_dirs = []
    for dir_str in potential_dirs:
        path = Path(dir_str)
        # Check if it's a directory and contains the essential metadata file
        if path.is_dir() and (path / "metadata.json").exists():
             # Basic check: ensure parent dir name looks like a hash (e.g. 8 hex chars)
             # and grandparent looks like build flags etc. This helps filter out
             # intermediate or incorrectly structured directories.
             parent_name = path.parent.name
             grandparent_name = path.parent.parent.name
             if len(parent_name) == 8 and all(c in '0123456789abcdef' for c in parent_name.lower()):
                 # Add more checks on grandparent etc. if needed
                valid_dirs.append(path)
             else:
                 logger.debug(f"Skipping directory - parent name '{parent_name}' doesn't look like metadata hash: {path}")

    logger.info(f"Found {len(valid_dirs)} potential result directories.")
    return valid_dirs


def load_benchmark_results_comparison(result_path: Path, experiment_name: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Loads benchmark data and metadata specifically for comparison.
    Used by generate_combined_report.
    Returns: Tuple of (benchmark_data, metadata) or (None, None).
    """
    experiment_dir = result_path / experiment_name
    if not experiment_dir.exists():
        logger.warning(f"Comparison: Experiment directory not found: {experiment_dir}")
        return None, None

    benchmark_file = experiment_dir / "benchmark_output.json"
    metadata_file = experiment_dir / "metadata.json"

    benchmark_data = load_gbench_json(benchmark_file)
    metadata = load_metadata_json(metadata_file)

    if benchmark_data is None:
        logger.warning(f"Comparison: Benchmark data missing for {experiment_name} in {result_path}")
    if metadata is None:
        logger.warning(f"Comparison: Metadata missing for {experiment_name} in {result_path}")
        # Allow comparison even if metadata is missing, but benchmark data exists
        metadata = {} # Provide empty dict

    return benchmark_data, metadata