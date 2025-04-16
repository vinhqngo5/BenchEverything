# scripts/run_benchmarks.py

#!/usr/bin/env python3

import argparse
import sys
import traceback
from pathlib import Path
import platform # Needed for fallback platform id

# Ensure the lib directory is in the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.logger import setup_logger, get_logger
from lib.config import BenchEverythingConfig
from lib.runner import BenchmarkRunner, BuildError, BenchmarkExecutionError
# lib.metadata import load_metadata # No longer needed here

# Setup logger first
setup_logger()
logger = get_logger()

def main():
    """Main function to run benchmarks."""
    parser = argparse.ArgumentParser(description='Build and run benchmarks, collect results.')
    parser.add_argument('--config',
                        help='Path to a custom configuration file (default: scripts/config/benchmark_config.json)')
    parser.add_argument('--compiler',
                        help='Comma-separated list of compiler names (from config) to use (default: all)')
    parser.add_argument('--experiments',
                        help='Comma-separated list of experiment names (from config) to run (default: all)')
    parser.add_argument('--build-flags', default='Release_O3',
                        help='Build flags identifier (e.g., Release_O3, Debug_O0, RelWithDebInfo_O2_native)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-run of benchmarks even if results exist')
    parser.add_argument('--incremental-build', action='store_true',
                        help='Use incremental build (faster for development, potentially less reproducible)')
    args = parser.parse_args()

    try:
        # --- Initialization ---
        logger.info("--- Starting Benchmark Run ---")
        config = BenchEverythingConfig(config_file=args.config)
        runner = BenchmarkRunner(config)

        # --- Determine Compilers ---
        all_compiler_configs = config.get_all_compiler_configs()
        if not all_compiler_configs:
            logger.error("No compilers defined in the configuration file.")
            sys.exit(1)

        target_compilers = []
        if args.compiler:
            requested_names = [name.strip() for name in args.compiler.split(',')]
            compiler_map = {cfg['name']: cfg for cfg in all_compiler_configs}
            for name in requested_names:
                if name in compiler_map:
                    target_compilers.append(compiler_map[name])
                else:
                    logger.warning(f"Requested compiler '{name}' not found in configuration. Skipping.")
            if not target_compilers:
                logger.error(f"None of the requested compilers ({args.compiler}) were found.")
                sys.exit(1)
        else:
            target_compilers = all_compiler_configs
            logger.info("Running with all configured compilers.")

        # --- Determine Experiments ---
        all_experiment_names = config.get_all_experiment_names()
        if not all_experiment_names:
             logger.error("No experiments defined in the configuration file.")
             sys.exit(1)

        target_experiments = []
        if args.experiments:
            requested_exp_names = [name.strip() for name in args.experiments.split(',')]
            exp_map = {name: True for name in all_experiment_names}
            for name in requested_exp_names:
                 if name in exp_map:
                      target_experiments.append(name)
                 else:
                      logger.warning(f"Requested experiment '{name}' not found in configuration. Skipping.")
            if not target_experiments:
                logger.error(f"None of the requested experiments ({args.experiments}) were found.")
                sys.exit(1)
        else:
            target_experiments = all_experiment_names
            logger.info("Running all configured experiments.")

        # --- Build and Run ---
        run_summary = {'success': 0, 'fail_build': 0, 'fail_run': 0, 'skipped': 0} # Removed 'total' here
        tasks_processed = 0 # Track tasks actually processed
        total_tasks_planned = len(target_compilers) * len(target_experiments)
        logger.info(f"Planning to run {len(target_experiments)} experiments across {len(target_compilers)} compilers "
                    f"with build flags '{args.build_flags}'. Total tasks planned: {total_tasks_planned}")


        for i, compiler_config in enumerate(target_compilers):
            compiler_name = compiler_config['name']
            logger.info(f"\n=== Processing Compiler: {compiler_name} ({i+1}/{len(target_compilers)}) ===")

            build_dir = None
            try:
                # Build all experiments for this compiler config once
                build_dir = runner.build_experiment(
                    compiler_name,
                    args.build_flags,
                    args.incremental_build
                )
                if not build_dir:
                    # Build failed, skip all experiments for this compiler
                    logger.error(f"Build failed for compiler {compiler_name}. Skipping its experiments.")
                    num_exps_affected = len(target_experiments)
                    run_summary['fail_build'] += num_exps_affected
                    tasks_processed += num_exps_affected # Count these as processed (failed)
                    continue # Skip to next compiler

                # Run each experiment using the successful build
                for j, experiment_name in enumerate(target_experiments):
                    task_num = i * len(target_experiments) + j + 1
                    logger.info(f"\n--- Task {task_num}/{total_tasks_planned}: Running {experiment_name} with {compiler_name} ({args.build_flags}) ---")
                    tasks_processed += 1 # Increment tasks processed counter
                    results_dir = None
                    status = "FAILED" # Default status
                    try:
                        # Run experiment returns (Optional[Path], status_string)
                        results_dir, status = runner.run_experiment(
                            experiment_name,
                            compiler_name,
                            args.build_flags,
                            build_dir,
                            args.force
                        )

                        # Update summary based on the returned status
                        if status == "RAN":
                            run_summary['success'] += 1
                        elif status == "SKIPPED":
                            run_summary['skipped'] += 1
                        else: # status == "FAILED" or results_dir is None
                            run_summary['fail_run'] += 1
                            # Log warning if not already logged by run_experiment
                            if results_dir is None:
                                 logger.warning(f"Experiment run failed pre-check for {experiment_name}")
                            # else: # Error happened during execution, already logged by run_experiment

                    except BenchmarkExecutionError as run_err:
                         logger.error(f"Benchmark execution failed for {experiment_name}: {run_err}")
                         run_summary['fail_run'] += 1
                    except Exception as exp_err:
                         logger.error(f"Unexpected error running experiment {experiment_name}: {exp_err}", exc_info=True)
                         run_summary['fail_run'] += 1


            except BuildError as build_err:
                logger.error(f"Build error encountered for compiler {compiler_name}: {build_err}")
                num_exps_affected = len(target_experiments)
                run_summary['fail_build'] += num_exps_affected # Count experiments affected
                tasks_processed += num_exps_affected # Count as processed
            except Exception as comp_err:
                logger.error(f"Unexpected error processing compiler {compiler_name}: {comp_err}", exc_info=True)
                # Assume build failed and mark all experiments for this compiler as failed
                num_exps_affected = len(target_experiments)
                run_summary['fail_build'] += num_exps_affected
                tasks_processed += num_exps_affected


        # --- Final Summary ---
        logger.info("\n--- Benchmark Run Summary ---")
        logger.info(f"Total Tasks Processed: {tasks_processed}") # Use actual processed count
        logger.info(f"Successful Runs:     {run_summary['success']}")
        logger.info(f"Skipped (exist):     {run_summary['skipped']}")
        logger.info(f"Failed Runs:         {run_summary['fail_run']}")
        logger.info(f"Failed Builds:       {run_summary['fail_build']} (counts each experiment affected)")
        logger.info("-----------------------------")

        # Exit code based only on failures, not skips
        exit_code = 0 if (run_summary['fail_run'] == 0 and run_summary['fail_build'] == 0) else 1
        sys.exit(exit_code)

    except Exception as e:
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()