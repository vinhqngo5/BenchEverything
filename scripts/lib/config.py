import json
import os
from pathlib import Path

from .logger import get_logger

logger = get_logger()

class BenchEverythingConfig:
    """Manages configuration loading and project paths."""

    def __init__(self, project_root=None, config_file=None):
        if project_root:
            self.project_root = Path(project_root).resolve()
        else:
            # Assumes this file is in scripts/lib/
            self.project_root = Path(__file__).resolve().parent.parent.parent

        self.config_file_path = self._resolve_config_path(config_file)
        self._global_config = None
        self._load_global_config()

        logger.debug(f"Project Root: {self.project_root}")
        logger.debug(f"Using Config File: {self.config_file_path}")

    def _resolve_config_path(self, config_file):
        """Find the benchmark_config.json file."""
        if config_file:
            path = Path(config_file)
            if path.is_absolute():
                return path
            else:
                return (self.project_root / path).resolve()
        else:
            return (self.project_root / "scripts" / "config" / "benchmark_config.json").resolve()

    def _load_global_config(self):
        """Load the main benchmark_config.json file."""
        if not self.config_file_path.exists():
            logger.error(f"Global configuration file not found: {self.config_file_path}")
            raise FileNotFoundError(f"Global configuration file not found: {self.config_file_path}")
        try:
            with open(self.config_file_path, 'r') as f:
                self._global_config = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing global config file {self.config_file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading global config file {self.config_file_path}: {e}")
            raise

    def get_project_root(self):
        """Return the project root directory Path object."""
        return self.project_root

    def get_global_config(self):
        """Return the loaded global configuration dictionary."""
        if self._global_config is None:
            self._load_global_config()
        return self._global_config

    def get_compiler_config(self, compiler_name):
        """Return the configuration dictionary for a specific compiler."""
        config = self.get_global_config()
        for compiler in config.get('compilers', []):
            if compiler.get('name') == compiler_name:
                return compiler
        logger.warning(f"Compiler configuration not found for: {compiler_name}")
        return None

    def get_all_compiler_configs(self):
        """Return a list of all compiler configuration dictionaries."""
        config = self.get_global_config()
        return config.get('compilers', [])

    def get_experiment_details(self, experiment_name):
        """Return the configuration dictionary for a specific experiment from the global config."""
        config = self.get_global_config()
        for exp in config.get('experiments', []):
            if exp.get('name') == experiment_name:
                return exp
        logger.warning(f"Experiment details not found in global config for: {experiment_name}")
        return None

    def get_all_experiment_names(self):
        """Return a list of all experiment names defined in the global config."""
        config = self.get_global_config()
        return [exp.get('name') for exp in config.get('experiments', []) if exp.get('name')]

    def load_experiment_config(self, experiment_name):
        """Load the experiment-specific configuration (exp_config.json), if it exists."""
        exp_config_path = self.project_root / "experiments" / experiment_name / "exp_config.json"
        if exp_config_path.exists():
            try:
                with open(exp_config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Error parsing experiment config for {experiment_name}: {e}")
            except Exception as e:
                logger.error(f"Error loading experiment config for {experiment_name}: {e}")
        return {} # Return empty dict if no config or error

    def get_build_dir(self, platform_id, compiler_id, build_flags_id):
        """Construct the Path object for the build directory."""
        return self.project_root / "build" / platform_id / compiler_id / build_flags_id

    def get_results_base_dir(self, platform_id, compiler_id, build_flags_id, metadata_hash):
         """Construct the Path object for the base results directory (up to hash)."""
         return self.project_root / "results" / platform_id / compiler_id / build_flags_id / metadata_hash

    def get_results_dir(self, platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name):
        """Construct the Path object for a specific experiment's results directory."""
        base_dir = self.get_results_base_dir(platform_id, compiler_id, build_flags_id, metadata_hash)
        return base_dir / experiment_name

    def get_report_base_dir(self, platform_id, compiler_id, build_flags_id, metadata_hash):
        """Construct the Path object for the base report directory (up to hash)."""
        return self.project_root / "reports" / platform_id / compiler_id / build_flags_id / metadata_hash

    def get_report_dir(self, platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name):
        """Construct the Path object for a specific experiment's report directory."""
        base_dir = self.get_report_base_dir(platform_id, compiler_id, build_flags_id, metadata_hash)
        return base_dir / experiment_name

    def get_report_assets_dir(self, platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name):
        """Construct the Path object for a specific experiment's report assets directory."""
        report_dir = self.get_report_dir(platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name)
        return report_dir / "assets"

    def get_comparison_report_dir(self, platform_id=None):
        """Constructs the directory for comparison reports."""
        reports_dir = self.project_root / "reports"
        if platform_id:
             # Use only the OS part for grouping comparisons if desired, or full id
             os_part = platform_id.split('-')[0] if platform_id else "unknown_platform"
             return reports_dir / os_part / "comparisons"
        else:
             return reports_dir / "comparisons"

    def get_assembly_dir(self, results_dir_path):
        """Construct the Path object for the assembly directory within a results directory."""
        return Path(results_dir_path) / "assembly"

    def get_template_path(self, experiment_name):
        """Find and return the Path object for the experiment's report template file."""
        exp_details = self.get_experiment_details(experiment_name)

        # 1. Check 'template_file' in global config
        if exp_details and 'template_file' in exp_details:
            template_path = self.project_root / exp_details['template_file']
            if template_path.exists():
                return template_path
            else:
                logger.warning(f"Template path from config not found: {template_path}")

        # 2. Fallback to default location in experiment directory
        fallback_path = self.project_root / "experiments" / experiment_name / "README.md.template"
        if fallback_path.exists():
            return fallback_path
        
        logger.error(f"Template file not found for experiment: {experiment_name}")
        return None

    def resolve_path(self, path_str):
        """Resolve a path string relative to the project root."""
        return (self.project_root / path_str).resolve()

    def validate_path(self, path):
        """Validate that a path exists and return a Path object."""
        path_obj = Path(path)
        if not path_obj.is_absolute():
             path_obj = self.resolve_path(str(path))

        if not path_obj.exists():
            logger.error(f"Path does not exist: {path_obj}")
            return None
        return path_obj