
import argparse
import sys
import os
import subprocess
from pathlib import Path

# Ensure the lib directory is in the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.logger import setup_logger, get_logger
from lib.config import BenchEverythingConfig
from lib.data_loader import find_all_result_dirs, load_benchmark_run
from lib.template import TemplateRenderer

# Setup logger first
setup_logger()
logger = get_logger()

def run_pre_report_script(experiment_name: str, results_dir: Path, assets_dir: Path, project_root: Path):
    """Run the pre_report.py script if it exists."""
    pre_report_script = project_root / "experiments" / experiment_name / "pre_report.py"
    if pre_report_script.exists():
        try:
            # Ensure assets directory exists
            os.makedirs(assets_dir, exist_ok=True)

            cmd = [
                sys.executable, # Use the current Python interpreter
                str(pre_report_script),
                "--results-dir", str(results_dir),
                "--output-dir", str(assets_dir)
            ]
            logger.info(f"Running pre-report script: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
            logger.info(f"Pre-report script completed successfully for {experiment_name}.")
            if result.stdout: logger.debug(f"Pre-report stdout: {result.stdout.strip()}")
            if result.stderr: logger.warning(f"Pre-report stderr: {result.stderr.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Pre-report script failed for {experiment_name} (return code {e.returncode}).")
            logger.error(f"Stdout:\n{e.stdout}")
            logger.error(f"Stderr:\n{e.stderr}")
            return False
        except subprocess.TimeoutExpired:
            logger.error(f"Pre-report script timed out for {experiment_name}.")
            return False
        except Exception as e:
             logger.error(f"Error running pre-report script for {experiment_name}: {e}", exc_info=True)
             return False
    else:
        logger.debug(f"No pre-report script found for {experiment_name} at {pre_report_script}")
        return True # Not a failure if script doesn't exist


def generate_single_report(results_dir: Path, config: BenchEverythingConfig) -> bool:
    """Generate a report for a single result directory."""
    logger.info(f"--- Generating Report for: {results_dir} ---")

    run_data = load_benchmark_run(results_dir)
    if not run_data or run_data.load_error or not run_data.metadata:
        logger.error(f"Failed to load necessary data from {results_dir}. Skipping report generation.")
        return False

    metadata = run_data.metadata
    experiment_name = metadata.get('experiment_name')
    if not experiment_name:
        logger.error(f"Experiment name missing in metadata for {results_dir}. Cannot generate report.")
        return False

    # Determine report directory and template path
    try:
        platform_id = metadata['detailed_platform_id']
        compiler_id = metadata['detailed_compiler_id']
        build_flags_id = metadata['build_flags_id']
        metadata_hash = metadata['metadata_hash']

        report_dir = config.get_report_dir(platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name)
        assets_dir = config.get_report_assets_dir(platform_id, compiler_id, build_flags_id, metadata_hash, experiment_name)
        template_path = config.get_template_path(experiment_name)

        if not template_path:
            # Error already logged by get_template_path
            return False

        os.makedirs(report_dir, exist_ok=True)
        # Assets dir created by pre-report script if needed, or here.
        os.makedirs(assets_dir, exist_ok=True)

    except KeyError as e:
        logger.error(f"Metadata key missing in {results_dir}/metadata.json, cannot determine report path: {e}")
        return False
    except Exception as e:
        logger.error(f"Error setting up report paths: {e}", exc_info=True)
        return False

    # Run pre-report script
    pre_report_success = run_pre_report_script(experiment_name, results_dir, assets_dir, config.get_project_root())
    if not pre_report_success:
         logger.warning(f"Pre-report script failed for {experiment_name}. Report may be incomplete.")
         # Continue generating report anyway? Yes.

    # Prepare context for template rendering
    context = {
        "experiment_name": experiment_name,
        "results_dir": results_dir, # Pass results dir for related links
        "gbench_data": run_data.gbench_data,
        "metadata": run_data.metadata,
        "perf_log": run_data.perf_log,
        "assembly_files": run_data.assembly_files, # Dict: name -> Path
    }

    # Render the template
    renderer = TemplateRenderer(template_path)
    rendered_content = renderer.render(context, report_dir, config.get_project_root())

    if rendered_content is None:
        logger.error(f"Failed to render report template for {experiment_name}.")
        return False

    # Write the report
    report_file_path = report_dir / "report.md"
    try:
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        logger.info(f"Report generated successfully: {report_file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing report to {report_file_path}: {e}")
        return False


def main():
    """Main function to generate reports."""
    parser = argparse.ArgumentParser(description='Generate Markdown reports from benchmark results.')
    parser.add_argument('--result-dir',
                        help='Path to a specific result directory (e.g., results/linux-x86_64/.../exp_name). '
                             'If not specified, reports will be generated for all available results.')
    parser.add_argument('--config',
                        help='Path to a custom configuration file (used for resolving paths).')
    args = parser.parse_args()

    try:
        config = BenchEverythingConfig(config_file=args.config)
        project_root = config.get_project_root()

        if args.result_dir:
            # Generate report for a specific directory
            result_dir_path = Path(args.result_dir)
            if not result_dir_path.is_absolute():
                 result_dir_path = (project_root / result_dir_path).resolve()

            if not result_dir_path.is_dir():
                logger.error(f"Specified result directory not found or not a directory: {result_dir_path}")
                sys.exit(1)

            success = generate_single_report(result_dir_path, config)
            sys.exit(0 if success else 1)
        else:
            # Generate reports for all found result directories
            logger.info("Searching for result directories to generate reports...")
            results_dirs = find_all_result_dirs(project_root)

            if not results_dirs:
                logger.info("No valid result directories found.")
                sys.exit(0)

            logger.info(f"Found {len(results_dirs)} result directories. Generating reports...")
            all_success = True
            successful_reports = 0
            failed_reports = 0

            for i, result_dir in enumerate(results_dirs):
                 logger.info(f"\n--- Processing Result Directory {i+1}/{len(results_dirs)}: {result_dir.relative_to(project_root)} ---")
                 try:
                     success = generate_single_report(result_dir, config)
                     if success:
                         successful_reports += 1
                     else:
                         failed_reports += 1
                         all_success = False
                 except Exception as e:
                     logger.error(f"Unexpected error generating report for {result_dir}: {e}", exc_info=True)
                     failed_reports += 1
                     all_success = False

            # Print summary
            logger.info("\n--- Report Generation Summary ---")
            logger.info(f"Total directories processed: {len(results_dirs)}")
            logger.info(f"Successfully generated reports: {successful_reports}")
            logger.info(f"Failed reports: {failed_reports}")
            logger.info("---------------------------------")

            sys.exit(0 if all_success else 1)

    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()