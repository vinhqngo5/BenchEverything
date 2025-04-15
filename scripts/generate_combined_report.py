#!/usr/bin/env python3

import os
import json
import argparse
import sys
import glob
import platform
import subprocess
import re
import hashlib
import logging
import math
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

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

def load_config():
    """Load benchmark configuration from JSON file."""
    config_path = PROJECT_ROOT / "scripts" / "config" / "benchmark_config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def find_all_experiment_names():
    """Find all experiment names from the configuration."""
    config = load_config()
    return [exp['name'] for exp in config.get('experiments', [])]

def validate_path(path):
    """Validate that a path exists and return a Path object."""
    path_obj = Path(path)
    if not path_obj.exists():
        logger.error(f"Path does not exist: {path}")
        return None
    return path_obj

def load_benchmark_results(result_path, experiment_name):
    """Load benchmark results for a specific experiment.
    
    Args:
        result_path: Path to the baseline or contender result directory
        experiment_name: Name of the experiment to load
        
    Returns:
        Tuple of (benchmark_data, metadata) or (None, None) if not found
    """
    experiment_dir = result_path / experiment_name
    if not experiment_dir.exists():
        logger.warning(f"Experiment directory not found: {experiment_dir}")
        return None, None
    
    # Load benchmark data
    benchmark_file = experiment_dir / "benchmark_output.json"
    if not benchmark_file.exists():
        logger.warning(f"Benchmark results file not found: {benchmark_file}")
        return None, None
    
    # Load metadata
    metadata_file = experiment_dir / "metadata.json"
    metadata = {}
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"Error parsing metadata for {experiment_name}: {e}")
    
    # Load benchmark data
    try:
        with open(benchmark_file, 'r') as f:
            benchmark_data = json.load(f)
        return benchmark_data, metadata
    except json.JSONDecodeError as e:
        logger.warning(f"Error parsing benchmark results for {experiment_name}: {e}")
        return None, None

def identify_common_metrics(baseline_data, contender_data):
    """Identify metrics that are common between baseline and contender data.
    
    Args:
        baseline_data: Benchmark data from baseline
        contender_data: Benchmark data from contender
        
    Returns:
        Set of common metric names
    """
    if not baseline_data or not contender_data:
        return set()
    
    # Define non-essential fields to exclude
    excluded_fields = {
        "repetition_index", "family_index", "per_family_instance_index", 
        "run_name", "run_type", "aggregate_name", "label"
    }
    
    baseline_metrics = set()
    contender_metrics = set()
    
    # Get metrics from first benchmark in baseline
    if 'benchmarks' in baseline_data and baseline_data['benchmarks']:
        first_benchmark = baseline_data['benchmarks'][0]
        for key, value in first_benchmark.items():
            if (key not in excluded_fields and 
                (isinstance(value, (int, float, bool)) or 
                 (isinstance(value, str) and value.replace('.', '', 1).isdigit()))):
                baseline_metrics.add(key)
    
    # Get metrics from first benchmark in contender
    if 'benchmarks' in contender_data and contender_data['benchmarks']:
        first_benchmark = contender_data['benchmarks'][0]
        for key, value in first_benchmark.items():
            if (key not in excluded_fields and 
                (isinstance(value, (int, float, bool)) or 
                 (isinstance(value, str) and value.replace('.', '', 1).isdigit()))):
                contender_metrics.add(key)
    
    # Return intersection of metrics
    return baseline_metrics.intersection(contender_metrics)

def calculate_improvement(baseline_value, contender_value, metric_name):
    """Calculate improvement percentage between baseline and contender.
    
    Args:
        baseline_value: Value from baseline
        contender_value: Value from contender
        metric_name: Name of the metric
        
    Returns:
        Improvement percentage (positive = improvement, negative = regression)
    """
    if baseline_value == 0:
        return float('inf') if contender_value < baseline_value else float('-inf')
    
    # For time-based metrics, lower is better
    if metric_name in ['real_time', 'cpu_time', 'time']:
        return ((baseline_value - contender_value) / baseline_value) * 100
    
    # For throughput metrics, higher is better
    return ((contender_value - baseline_value) / baseline_value) * 100

def get_winner(improvement):
    """Determine which configuration is better based on improvement percentage.
    
    Args:
        improvement: Improvement percentage
        
    Returns:
        'baseline', 'contender', or 'tie'
    """
    if abs(improvement) < 1.0:  # Less than 1% difference is considered a tie
        return 'tie'
    return 'contender' if improvement > 0 else 'baseline'

def create_comparison_table(baseline_data, contender_data, baseline_label, contender_label, common_metrics):
    """Create a Markdown comparison table for baseline and contender.
    
    Args:
        baseline_data: Benchmark data from baseline
        contender_data: Benchmark data from contender
        baseline_label: Label for baseline
        contender_label: Label for contender
        common_metrics: Set of common metric names
        
    Returns:
        Markdown table as string
    """
    if not baseline_data or not contender_data or not common_metrics:
        return "[No comparable data available]"
    
    # Map display names for common metrics
    metric_display = {
        'name': 'Benchmark',
        'real_time': 'Time (ns)',
        'cpu_time': 'CPU (ns)',
        'iterations': 'Iterations',
        'threads': 'Threads',
        'time_unit': 'Time Unit',
        'repetitions': 'Repetitions',
        'time_cv': 'Time CV (%)',
        'cpu_cv': 'CPU CV (%)',
        'items_per_second': 'Items/Second',
        'bytes_per_second': 'Bytes/Second'
    }
    
    # Create table headers
    headers = ['Benchmark']
    
    # Order metrics with core metrics first 
    ordered_metrics = []
    core_metrics = ['real_time', 'cpu_time', 'iterations']
    
    # Add core metrics first
    for metric in core_metrics:
        if metric in common_metrics:
            ordered_metrics.append(metric)
    
    # Add remaining metrics
    for metric in sorted(common_metrics):
        if metric != 'name' and metric not in core_metrics:
            ordered_metrics.append(metric)
    
    # Build headers for each metric
    for metric in ordered_metrics:
        display_name = metric_display.get(metric, metric)
        headers.append(f"{baseline_label} {display_name}")
        headers.append(f"{contender_label} {display_name}")
        headers.append(f"Improvement (%)")
    
    headers.append("Winner")
    
    # Create header row
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["-" * len(header) for header in headers]) + " |\n"
    
    # Create a map of benchmark name to data for easier lookup
    baseline_benchmarks = {b['name']: b for b in baseline_data.get('benchmarks', [])}
    contender_benchmarks = {b['name']: b for b in contender_data.get('benchmarks', [])}
    
    # Get common benchmark names
    common_benchmarks = set(baseline_benchmarks.keys()).intersection(set(contender_benchmarks.keys()))
    
    # Add rows for each common benchmark
    for bench_name in sorted(common_benchmarks):
        baseline_bench = baseline_benchmarks[bench_name]
        contender_bench = contender_benchmarks[bench_name]
        
        row = [bench_name]
        best_improvement = -float('inf')  # Track best improvement for winner
        worst_regression = float('inf')   # Track worst regression
        
        # Process metrics in order
        for metric in ordered_metrics:
            baseline_value = baseline_bench.get(metric, 0)
            contender_value = contender_bench.get(metric, 0)
            
            # Convert to float for calculation if possible
            try:
                baseline_float = float(baseline_value)
                contender_float = float(contender_value)
                
                # Calculate improvement
                improvement = calculate_improvement(baseline_float, contender_float, metric)
                
                # Track best improvement / worst regression
                if improvement > 0 and improvement > best_improvement:
                    best_improvement = improvement
                elif improvement < 0 and improvement < worst_regression:
                    worst_regression = improvement
                
                # Format values for table
                if isinstance(baseline_value, (int, float)) and metric not in ["iterations", "threads", "repetitions"]:
                    row.append(f"{baseline_float:.2f}")
                else:
                    row.append(f"{baseline_value}")
                    
                if isinstance(contender_value, (int, float)) and metric not in ["iterations", "threads", "repetitions"]:
                    row.append(f"{contender_float:.2f}")
                else:
                    row.append(f"{contender_value}")
                
                # Format improvement
                if math.isfinite(improvement):
                    color = ""
                    if improvement > 0:
                        color = "green"
                    elif improvement < 0:
                        color = "red"
                    
                    row.append(f"<span style='color:{color}'>{improvement:.2f}%</span>")
                else:
                    if improvement > 0:
                        row.append("<span style='color:green'>∞</span>")
                    else:
                        row.append("<span style='color:red'>∞</span>")
            except (ValueError, TypeError):
                # Handle non-numeric values
                row.append(f"{baseline_value}")
                row.append(f"{contender_value}")
                row.append("N/A")
        
        # Determine overall winner based on best improvement or worst regression
        winner = "tie"
        if best_improvement > 1.0:  # Significant improvement
            winner = contender_label
        elif worst_regression < -1.0:  # Significant regression
            winner = baseline_label
            
        row.append(winner)
        
        # Add row to table
        table += "| " + " | ".join(row) + " |\n"
    
    # Check if iterations or repetitions differ between baseline and contender
    warnings = []
    
    # Check iterations differ
    if 'iterations' in common_metrics:
        baseline_iterations = set(int(b.get('iterations', 0)) for b in baseline_data.get('benchmarks', []))
        contender_iterations = set(int(b.get('iterations', 0)) for b in contender_data.get('benchmarks', []))
        
        if baseline_iterations != contender_iterations:
            warnings.append(f"**Iterations differ:** Baseline: {sorted(baseline_iterations)}, Contender: {sorted(contender_iterations)}")
    
    # Check if repetitions differ
    if 'repetitions' in common_metrics:
        baseline_repetitions = set(int(b.get('repetitions', 1)) for b in baseline_data.get('benchmarks', []))
        contender_repetitions = set(int(b.get('repetitions', 1)) for b in contender_data.get('benchmarks', []))
        
        if baseline_repetitions != contender_repetitions:
            warnings.append(f"**Repetitions differ:** Baseline: {sorted(baseline_repetitions)}, Contender: {sorted(contender_repetitions)}")
    
    # Add warnings if any
    if warnings:
        table += "\n**Note:** Google Benchmark has determined different workloads for baseline and contender, which may affect result quality:\n"
        for warning in warnings:
            table += f"- {warning}\n"
    
    return table

def extract_config_info(path):
    """Extract configuration information from a path.
    
    Args:
        path: Path to a result directory
        
    Returns:
        Tuple of (platform, compiler, flags, hash) or empty strings if not found
    """
    try:
        parts = path.parts
        
        # Try to find the 'results' index
        if 'results' in parts:
            idx = parts.index('results')
            if len(parts) >= idx + 5:  # results/platform/compiler/flags/hash
                platform = parts[idx + 1]
                compiler = parts[idx + 2]
                flags = parts[idx + 3]
                metadata_hash = parts[idx + 4]
                return platform, compiler, flags, metadata_hash
    except Exception as e:
        logger.debug(f"Error extracting config info from path: {e}")
    
    # Fallback: Use path parts if available
    try:
        if len(path.parts) >= 4:
            # Assume the last 4 parts are platform/compiler/flags/hash
            return path.parts[-4], path.parts[-3], path.parts[-2], path.parts[-1]
    except Exception:
        pass
        
    # Last resort: Read from metadata if available
    try:
        # Try a common experiment to find metadata
        experiment_dirs = [d for d in path.iterdir() if d.is_dir()]
        if experiment_dirs:
            metadata_file = experiment_dirs[0] / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                platform = metadata.get('detailed_platform_id', '')
                compiler = metadata.get('detailed_compiler_id', '')
                flags = metadata.get('build_flags_id', '')
                metadata_hash = metadata.get('metadata_hash', '')
                return platform, compiler, flags, metadata_hash
    except Exception:
        pass
    
    return '', '', '', ''

def get_configuration_label(path):
    """Generate a user-friendly label for a configuration.
    
    Args:
        path: Path to a result directory
        
    Returns:
        User-friendly label like "GCC 11.2 (Release_O3)"
    """
    platform, compiler, flags, _ = extract_config_info(path)
    
    # Try to extract compiler name and version
    compiler_parts = compiler.split('-', 1)
    compiler_name = compiler_parts[0] if compiler_parts else ''
    compiler_version = compiler_parts[1] if len(compiler_parts) > 1 else ''
    
    # Create a user-friendly label
    if compiler_name and flags:
        return f"{compiler_name.upper()} {compiler_version} ({flags})"
    elif compiler:
        return compiler
    else:
        return path.name

def get_original_report_path(results_dir, experiment_name):
    """Get the path to the original report for a specific experiment.
    
    Args:
        results_dir: Path to the results directory (baseline or contender)
        experiment_name: Name of the experiment
        
    Returns:
        Path to the original report if it exists, or None
    """
    # Extract components from results path
    platform, compiler, flags, metadata_hash = extract_config_info(results_dir)
    
    # Check if report exists
    report_path = PROJECT_ROOT / "reports" / platform / compiler / flags / metadata_hash / experiment_name / "report.md"
    
    if report_path.exists():
        return report_path
    
    return None

def get_results_dir_link(results_dir, experiment_name):
    """Get the path to the original results directory for a specific experiment.
    
    Args:
        results_dir: Path to the baseline or contender result directory (root of all experiments)
        experiment_name: Name of the experiment
        
    Returns:
        Path to the results directory for the experiment
    """
    # This will always return a path, even if it doesn't exist
    return results_dir / experiment_name

def create_metadata_comparison_table(baseline_metadata, contender_metadata):
    """Create a table comparing key metadata between baseline and contender.
    
    Args:
        baseline_metadata: Metadata from baseline
        contender_metadata: Metadata from contender
    
    Returns:
        Markdown table as string
    """
    if not baseline_metadata or not contender_metadata:
        return "[No metadata comparison available]"
    
    table = "| Property | Baseline | Contender |\n"
    table += "|----------|----------|----------|\n"
    
    # List of key properties to compare
    key_properties = [
        ("Platform", "detailed_platform_id"),
        ("CPU Model", "cpu_model"),
        ("Compiler", "compiler_id"),
        ("Compiler Version", "compiler_version"),
        ("Build Flags", "build_flags_id"),
        ("Date", "timestamp_iso")
    ]
    
    for display_name, property_name in key_properties:
        baseline_value = baseline_metadata.get(property_name, "Unknown")
        contender_value = contender_metadata.get(property_name, "Unknown")
        
        # Highlight differences
        if baseline_value != contender_value:
            table += f"| **{display_name}** | {baseline_value} | {contender_value} |\n"
        else:
            table += f"| {display_name} | {baseline_value} | {contender_value} |\n"
    
    return table

def get_path_for_report(path, report_dir=None):
    """Convert a path to a format suitable for inclusion in a report.
    
    Args:
        path: Path object or string to convert
        report_dir: Optional report directory to make paths relative to
        
    Returns:
        String representation of the path suitable for a Markdown link
    """
    path_obj = Path(path)
    path_str = str(path_obj)
    
    # If report_dir is provided, calculate a true relative path
    if report_dir:
        try:
            # For relative paths like 'results/...', prepend project root to make them absolute
            if path_str.startswith('results/') or path_str.startswith('reports/'):
                absolute_path = PROJECT_ROOT / path_str
                relative_path = os.path.relpath(absolute_path, report_dir)
                return relative_path
            
            # For already absolute paths, make them relative to the report directory
            relative_path = os.path.relpath(path_obj, report_dir)
            return relative_path
        except Exception as e:
            logger.debug(f"Error calculating relative path: {e}")
    
    # Fallbacks for when report_dir is not provided or relative path calculation fails
    try:
        # Try to make it relative to project root
        return str(path_obj.relative_to(PROJECT_ROOT))
    except ValueError:
        # If that fails, use aggressive cleanup
        pass
    
    # Check for paths that contain duplicated segments like reports/platform/reports/platform/...
    prefixes = ['reports/', 'results/']
    for prefix in prefixes:
        if path_str.count(prefix) > 1:
            # Find second occurrence
            first_pos = path_str.find(prefix)
            second_pos = path_str.find(prefix, first_pos + 1)
            
            if (second_pos != -1):
                # Take everything from the second occurrence forward
                clean_path = path_str[second_pos:]
                return clean_path
    
    # If the path starts with reports/ or results/, use it as is
    if path_str.startswith('reports/') or path_str.startswith('results/'):
        return path_str
    
    # Return absolute path as a last resort
    return path_str

def create_multi_comparison_report(baseline_dir, contender_dirs, experiment_names=None, output_dir=None):
    """Create a comparison report between baseline and multiple contender configurations.
    
    Args:
        baseline_dir: Path to baseline results directory
        contender_dirs: List of paths to contender result directories
        experiment_names: List of experiment names to include (default: all)
        output_dir: Directory to save the report (default: auto-generated)
        
    Returns:
        Path to the generated report
    """
    # Validate directories
    baseline_dir = validate_path(baseline_dir)
    if not baseline_dir:
        logger.error("Invalid baseline directory")
        return None
    
    valid_contenders = []
    for contender_dir in contender_dirs:
        valid_path = validate_path(contender_dir)
        if valid_path:
            valid_contenders.append(valid_path)
        else:
            logger.warning(f"Skipping invalid contender directory: {contender_dir}")
    
    if not valid_contenders:
        logger.error("No valid contender directories provided")
        return None
    
    # Get configuration labels
    baseline_label = get_configuration_label(baseline_dir)
    contender_labels = [get_configuration_label(contender) for contender in valid_contenders]
    
    # Create report directory
    if not output_dir:
        # Create report directory based on platform
        platform_info, _, _, _ = extract_config_info(baseline_dir)
        reports_dir = PROJECT_ROOT / "reports"
        
        if platform_info:
            report_dir = reports_dir / platform_info / "comparisons"
        else:
            report_dir = reports_dir / "comparisons"
        
        # Create a comparison name based on the number of configurations
        if len(valid_contenders) == 1:
            # Simple comparison name for single contender
            _, b_compiler, b_flags, _ = extract_config_info(baseline_dir)
            _, c_compiler, c_flags, _ = extract_config_info(valid_contenders[0])
            
            if b_compiler and c_compiler:
                comparison_name = f"{b_compiler}_vs_{c_compiler}"
            elif b_flags and c_flags:
                comparison_name = f"{b_flags}_vs_{c_flags}"
            else:
                comparison_name = f"{baseline_dir.name}_vs_{valid_contenders[0].name}"
        else:
            # Multi-comparison name
            contender_count = len(valid_contenders)
            _, compiler, flags, _ = extract_config_info(baseline_dir)
            comparison_name = f"{compiler}_{flags}_vs_{contender_count}_contenders"
    else:
        report_dir = Path(output_dir)
        
        if len(valid_contenders) == 1:
            comparison_name = f"{baseline_label}_vs_{contender_labels[0]}".replace(' ', '_')
        else:
            comparison_name = f"{baseline_label}_vs_multiple_contenders".replace(' ', '_')
    
    # Ensure report directory exists
    os.makedirs(report_dir, exist_ok=True)
    
    # Get experiment names to compare
    if not experiment_names:
        experiment_names = find_all_experiment_names()
    elif isinstance(experiment_names, str):
        experiment_names = experiment_names.split(',')
    
    # Start building the report content
    if len(valid_contenders) == 1:
        report_content = f"# Comparison Report: {baseline_label} vs {contender_labels[0]}\n\n"
    else:
        report_content = f"# Multi-Configuration Comparison Report\n\n"
    
    report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Add table of contents
    report_content += "## Table of Contents\n\n"
    report_content += "1. [Configuration Details](#configuration-details)\n"
    report_content += "2. [Summary of Results](#summary-of-results)\n"
    
    idx = 3
    for experiment_name in experiment_names:
        report_content += f"{idx}. [{experiment_name}](#{experiment_name.lower().replace(' ', '-')})\n"
        idx += 1
    
    report_content += f"{idx}. [Failed Comparisons](#failed-comparisons)\n\n"
    
    # Add configuration section
    report_content += "## Configuration Details\n\n"
    report_content += f"### Baseline: {baseline_label}\n"
    report_content += f"Path: `{baseline_dir}`\n\n"
    
    for i, (contender_dir, contender_label) in enumerate(zip(valid_contenders, contender_labels)):
        report_content += f"### Contender {i+1}: {contender_label}\n"
        report_content += f"Path: `{contender_dir}`\n\n"
    
    # Process each experiment
    successful_experiments = []
    failed_experiments = []
    
    # Collect summary data for all experiments
    summary_data = []
    
    for experiment_name in experiment_names:
        logger.info(f"Processing experiment: {experiment_name}")
        
        # Load baseline benchmark results
        baseline_data, baseline_metadata = load_benchmark_results(baseline_dir, experiment_name)
        
        # Skip if baseline data is missing
        if not baseline_data:
            logger.warning(f"Baseline data missing for experiment: {experiment_name}")
            failed_experiments.append((experiment_name, "Baseline data missing"))
            continue
        
        # Start experiment section in report
        report_content += f"## {experiment_name}\n\n"
        
        # Process each contender for this experiment
        exp_summary_data = {}  # Track summary data for this experiment
        valid_contender_count = 0
        
        # Add links to original reports and result directories for baseline
        report_content += "### Original Reports and Data\n\n"
        report_content += "#### Baseline\n"
        baseline_report = get_original_report_path(baseline_dir, experiment_name)
        baseline_results = get_results_dir_link(baseline_dir, experiment_name)
        
        if baseline_report:
            report_content += f"- [Report]({get_path_for_report(baseline_report, report_dir)})\n"
        else:
            report_content += "- Report: Not available\n"
        
        report_content += f"- [Raw Results]({get_path_for_report(baseline_results, report_dir)})\n\n"
        
        for i, (contender_dir, contender_label) in enumerate(zip(valid_contenders, contender_labels)):
            # Load contender benchmark results
            contender_data, contender_metadata = load_benchmark_results(contender_dir, experiment_name)
            
            # Skip this contender if data is missing
            if not contender_data:
                logger.warning(f"Contender {i+1} data missing for experiment: {experiment_name}")
                failed_experiments.append((experiment_name, f"Contender {i+1} ({contender_label}) data missing"))
                continue
            
            # Identify common metrics
            common_metrics = identify_common_metrics(baseline_data, contender_data)
            
            if not common_metrics:
                logger.warning(f"No common metrics found for experiment {experiment_name} with contender {i+1}")
                failed_experiments.append((experiment_name, f"No common metrics with contender {i+1} ({contender_label})"))
                continue
            
            # Add contender report link
            report_content += f"#### Contender {i+1}: {contender_label}\n"
            contender_report = get_original_report_path(contender_dir, experiment_name)
            contender_results = get_results_dir_link(contender_dir, experiment_name)
            
            if contender_report:
                report_content += f"- [Report]({get_path_for_report(contender_report, report_dir)})\n"
            else:
                report_content += "- Report: Not available\n"
            
            report_content += f"- [Raw Results]({get_path_for_report(contender_results, report_dir)})\n\n"
            
            # Add metadata comparison table
            if baseline_metadata and contender_metadata:
                report_content += f"### Configuration Comparison: Baseline vs {contender_label}\n\n"
                metadata_comparison = create_metadata_comparison_table(baseline_metadata, contender_metadata)
                report_content += metadata_comparison + "\n\n"
            
            # Create comparison table
            report_content += f"### Benchmark Comparison: Baseline vs {contender_label}\n\n"
            comparison_table = create_comparison_table(
                baseline_data, contender_data, baseline_label, contender_label, common_metrics
            )
            report_content += comparison_table + "\n\n"
            
            # Add data to summary for this contender
            primary_metric = 'real_time' if 'real_time' in common_metrics else 'cpu_time'
            if primary_metric in common_metrics:
                # Calculate average improvement for the experiment
                improvements = []
                baseline_benchmarks = {b['name']: b for b in baseline_data.get('benchmarks', [])}
                contender_benchmarks = {b['name']: b for b in contender_data.get('benchmarks', [])}
                common_benchmarks = set(baseline_benchmarks.keys()).intersection(set(contender_benchmarks.keys()))
                
                for bench_name in common_benchmarks:
                    baseline_value = float(baseline_benchmarks[bench_name].get(primary_metric, 0))
                    contender_value = float(contender_benchmarks[bench_name].get(primary_metric, 0))
                    improvement = calculate_improvement(baseline_value, contender_value, primary_metric)
                    if math.isfinite(improvement):
                        improvements.append(improvement)
                
                avg_improvement = sum(improvements) / len(improvements) if improvements else 0
                exp_summary_data[contender_label] = (avg_improvement, len(common_benchmarks))
                valid_contender_count += 1
        
        # Add experiment to successful list if at least one contender was successfully compared
        if valid_contender_count > 0:
            successful_experiments.append(experiment_name)
            summary_data.append((experiment_name, exp_summary_data))
        else:
            # If no contenders were successfully compared, add to failed list
            if experiment_name not in [f[0] for f in failed_experiments]:
                failed_experiments.append((experiment_name, "No valid contenders for comparison"))
    
    # Add summary section after processing all experiments
    report_content = report_content.replace("## Summary of Results\n\n", "")  # Remove placeholder
    summary_section = "## Summary of Results\n\n"
    
    if summary_data:
        # Create summary table headers with all contenders
        headers = ["Experiment"]
        for contender_label in contender_labels:
            headers.append(f"{contender_label} Improvement (%)")
        headers.append("Best Contender")
        
        summary_section += "| " + " | ".join(headers) + " |\n"
        summary_section += "| " + " | ".join(["-" * len(header) for header in headers]) + " |\n"
        
        # Add data for each experiment
        for experiment_name, exp_data in summary_data:
            row = [experiment_name]
            
            # Find best contender for this experiment
            best_improvement = -float('inf')
            best_contender = ""
            
            # Add improvement data for each contender
            for contender_label in contender_labels:
                if contender_label in exp_data:
                    avg_improvement, _ = exp_data[contender_label]
                    
                    # Track best contender
                    if avg_improvement > best_improvement:
                        best_improvement = avg_improvement
                        best_contender = contender_label
                    
                    # Format improvement value
                    color = "green" if avg_improvement > 0 else "red" if avg_improvement < 0 else ""
                    formatted_improvement = f"<span style='color:{color}'>{avg_improvement:.2f}%</span>" if color else f"{avg_improvement:.2f}%"
                    row.append(formatted_improvement)
                else:
                    row.append("N/A")
            
            # Add best contender
            row.append(best_contender if best_contender else "None")
            
            # Add row to table
            summary_section += "| " + " | ".join(row) + " |\n"
    
    # Insert summary section after table of contents
    toc_end_idx = report_content.find("## Configuration Details")
    if toc_end_idx != -1:
        report_content = report_content[:toc_end_idx] + summary_section + "\n" + report_content[toc_end_idx:]
    
    # Add failed comparisons section
    if failed_experiments:
        report_content += "## Failed Comparisons\n\n"
        report_content += "| Experiment | Reason |\n"
        report_content += "|------------|--------|\n"
        
        for experiment, reason in failed_experiments:
            report_content += f"| {experiment} | {reason} |\n"
    
    # Write report to file
    report_file = report_dir / f"{comparison_name}_report.md"
    try:
        with open(report_file, 'w') as f:
            f.write(report_content)
        logger.info(f"Report generated successfully: {report_file}")
        return report_file
    except Exception as e:
        logger.error(f"Error writing report: {e}")
        return None

def main():
    """Main function to generate combined reports."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate a combined comparison report from benchmark results')
    parser.add_argument('--baseline', required=True,
                        help='Path to the baseline result directory')
    parser.add_argument('--contender', 
                        help='Path to a single contender result directory')
    parser.add_argument('--contenders',
                        help='Comma-separated list of paths to multiple contender result directories')
    parser.add_argument('--experiments',
                        help='Comma-separated list of experiments to include (default: all)')
    parser.add_argument('--output-dir',
                        help='Directory to save the report (default: auto-generated)')
    args = parser.parse_args()
    
    # Ensure we have at least one contender specified
    if not args.contender and not args.contenders:
        logger.error("Either --contender or --contenders must be specified")
        sys.exit(1)
    
    # Process contenders: combine single contender and multiple contenders if both are provided
    contenders = []
    if args.contender:
        contenders.append(args.contender)
    if args.contenders:
        contenders.extend(args.contenders.split(','))
    
    # Get experiment names
    experiment_names = None
    if args.experiments:
        experiment_names = args.experiments.split(',')
    
    # Create comparison report with multiple contenders
    report_file = create_multi_comparison_report(
        args.baseline,
        contenders,
        experiment_names,
        args.output_dir
    )
    
    # Exit with appropriate status code
    sys.exit(0 if report_file else 1)

if __name__ == "__main__":
    main()