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

def find_experiment_config(experiment_name):
    """Find the experiment configuration in the benchmark_config.json."""
    config = load_config()
    for exp in config.get('experiments', []):
        if exp.get('name') == experiment_name:
            return exp
    return None

def find_template_file(experiment_name):
    """Find the template file for the given experiment."""
    exp_config = find_experiment_config(experiment_name)
    if exp_config and 'template_file' in exp_config:
        template_path = PROJECT_ROOT / exp_config['template_file']
        if template_path.exists():
            return template_path
    
    # Fallback to looking in the experiment directory
    template_path = PROJECT_ROOT / "experiments" / experiment_name / "README.md.template"
    if template_path.exists():
        return template_path
    
    return None

def run_pre_report_script(experiment_name, results_dir, assets_dir):
    """Run the pre_report.py script if it exists."""
    pre_report_script = PROJECT_ROOT / "experiments" / experiment_name / "pre_report.py"
    if pre_report_script.exists():
        try:
            cmd = [
                "python", str(pre_report_script),
                "--results-dir", str(results_dir),
                "--output-dir", str(assets_dir)
            ]
            logger.info(f"Running pre-report script: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            logger.info(f"Pre-report script completed successfully")
            return True
        except subprocess.SubprocessError as e:
            logger.warning(f"Pre-report script failed: {e}")
    return False

def create_report_directories(results_dir):
    """Create report directories based on results directory structure."""
    # Extract components from the results path
    # Expected pattern: <results>/platform/compiler/flags/metadata_hash/experiment
    try:
        # Handle both Path objects and strings
        results_path = Path(results_dir) if not isinstance(results_dir, Path) else results_dir
        
        # Get the experiment name from the last part of the path
        experiment_name = results_path.name
        
        # Check if the path follows the expected structure
        if len(results_path.parts) >= 5:  # At least results/platform/compiler/flags/metadata_hash/experiment
            # Find the index of 'results' in the path
            try:
                results_index = results_path.parts.index('results')
                # Extract components after 'results'
                platform_id = results_path.parts[results_index + 1]
                compiler_id = results_path.parts[results_index + 2]
                build_flags_id = results_path.parts[results_index + 3]
                metadata_hash = results_path.parts[results_index + 4]
                
                # Create report directory
                report_base_dir = PROJECT_ROOT / "reports" / platform_id / compiler_id / build_flags_id / metadata_hash
                report_dir = report_base_dir / experiment_name
                assets_dir = report_dir / "assets"
                
                # Create directories
                os.makedirs(report_dir, exist_ok=True)
                os.makedirs(assets_dir, exist_ok=True)
                
                return report_dir, assets_dir, experiment_name
            except ValueError:
                # 'results' not found in path
                pass
    except Exception as e:
        logger.error(f"Error parsing results directory: {e}")
    
    # Fallback approach: Try to extract information from the results directory name
    try:
        experiment_name = results_path.name
        # Create a simple report directory without the full structure
        report_dir = PROJECT_ROOT / "reports" / experiment_name
        assets_dir = report_dir / "assets"
        
        # Create directories
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(assets_dir, exist_ok=True)
        
        return report_dir, assets_dir, experiment_name
    except Exception as e:
        logger.error(f"Error creating report directories: {e}")
        sys.exit(1)

def parse_benchmark_results(results_dir):
    """Parse Google Benchmark results from benchmark_output.json."""
    benchmark_file = results_dir / "benchmark_output.json"
    if not benchmark_file.exists():
        logger.error(f"Benchmark results file not found: {benchmark_file}")
        return None
    
    try:
        with open(benchmark_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing benchmark results: {e}")
        return None

def parse_metadata(results_dir):
    """Parse metadata from metadata.json."""
    metadata_file = results_dir / "metadata.json"
    if not metadata_file.exists():
        logger.warning(f"Metadata file not found: {metadata_file}")
        return {}
    
    try:
        with open(metadata_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing metadata: {e}")
        return {}

def parse_perf_data(results_dir):
    """Parse performance data from perf_stat.log."""
    perf_file = results_dir / "perf_stat.log"
    if not perf_file.exists():
        return "Performance counter data not available"
    
    try:
        with open(perf_file, 'r') as f:
            perf_data = f.read()
        
        # Simple formatting for perf data
        # In a real implementation, you might want to parse and format this more nicely
        return perf_data
    except Exception as e:
        logger.error(f"Error parsing perf data: {e}")
        return "Error parsing performance counter data"

def find_assembly_files(results_dir):
    """Find assembly files in the results directory."""
    assembly_dir = results_dir / "assembly"
    if not assembly_dir.exists():
        return {}
    
    assembly_files = {}
    for asm_file in assembly_dir.glob("*.s"):
        func_name = asm_file.stem
        try:
            with open(asm_file, 'r') as f:
                assembly_files[func_name] = f.read()
        except Exception as e:
            logger.error(f"Error reading assembly file {asm_file}: {e}")
            assembly_files[func_name] = f"Error reading assembly for {func_name}"
    
    return assembly_files

def create_benchmark_table(benchmark_results):
    """Create a Markdown table from benchmark results."""
    if not benchmark_results:
        return "[No benchmark results available]"
    
    # Get all metrics from the first benchmark to determine table columns
    columns = {}
    if benchmark_results.get('benchmarks') and len(benchmark_results['benchmarks']) > 0:
        first_benchmark = benchmark_results['benchmarks'][0]
        # Filter out non-numeric values or complex structures and map to user-friendly names
        column_mapping = {
            "name": "Benchmark",
            "real_time": "Time (ns)",
            "cpu_time": "CPU (ns)",
            "iterations": "Iterations",
            "threads": "Threads",
            "time_unit": "Time Unit",
            "repetitions": "Repetitions",
            "time_cv": "Time CV (%)",
            "cpu_cv": "CPU CV (%)",
            "items_per_second": "Items/Second",
            "bytes_per_second": "Bytes/Second"
            # Add any other metrics you want to display with user-friendly names
        }
        
        # Add core columns first in a specific order
        core_columns = ["name", "real_time", "cpu_time", "iterations"]
        for key in core_columns:
            if key in first_benchmark:
                columns[key] = column_mapping.get(key, key)
        
        # Then add any other numeric columns
        for key, value in first_benchmark.items():
            if key not in core_columns and (isinstance(value, (int, float, bool)) or 
                                           (isinstance(value, str) and value.replace('.', '', 1).isdigit())):
                if key in column_mapping:
                    columns[key] = column_mapping.get(key, key)
    
    # If no valid columns found, use defaults
    if not columns:
        columns = {
            "name": "Benchmark",
            "real_time": "Time (ns)",
            "cpu_time": "CPU (ns)",
            "iterations": "Iterations"
        }
    
    # Create table header based on found columns
    header_row = "| "
    separator_row = "| "
    
    for col_key, col_name in columns.items():
        header_row += f"{col_name} | "
        separator_row += "-" * len(col_name) + " | "
    
    table = header_row + "\n" + separator_row + "\n"
    
    try:
        for benchmark in benchmark_results.get('benchmarks', []):
            row = "| "
            for col_key in columns.keys():
                value = benchmark.get(col_key, "N/A")
                
                # Format numeric values
                if isinstance(value, (int, float)) and col_key not in ["iterations", "threads", "repetitions"]:
                    row += f"{value:.2f} | "
                else:
                    row += f"{value} | "
            
            table += row + "\n"
    except Exception as e:
        logger.error(f"Error creating benchmark table: {e}")
        return "[Error creating benchmark table]"
    
    return table

def create_metadata_table(metadata):
    """Create a Markdown table from metadata."""
    if not metadata:
        return "[No metadata available]"
    
    table = "| Property | Value |\n"
    table += "|----------|-------|\n"
    
    try:
        # Add key metadata fields
        table += f"| Timestamp | {metadata.get('timestamp_iso', 'Unknown')} |\n"
        table += f"| Platform | {metadata.get('platform_id', 'Unknown')} |\n"
        table += f"| Compiler | {metadata.get('compiler_id', 'Unknown')} |\n"
        table += f"| Build Flags | {metadata.get('build_flags_id', 'Unknown')} |\n"
        table += f"| Metadata Hash | {metadata.get('metadata_hash', 'Unknown')} |\n"
        
        # Add compiler flags
        config = metadata.get('config', {})
        table += f"| C++ Flags | {config.get('cxx_flags_used', 'Unknown')} |\n"
        table += f"| CMake Build Type | {config.get('cmake_build_type', 'Unknown')} |\n"
    except Exception as e:
        logger.error(f"Error creating metadata table: {e}")
        return "[Error creating metadata table]"
    
    return table

def create_assembly_links(assembly_files):
    """Create Markdown links to assembly files."""
    if not assembly_files:
        return "[No assembly files available]"
    
    links = ""
    for func_name in assembly_files:
        links += f"- [{func_name}](#assembly-for-{func_name})\n"
    
    return links

def find_assets(assets_dir, pattern):
    """Find assets matching the given pattern."""
    if not assets_dir.exists():
        return []
    
    return list(assets_dir.glob(pattern))

def replace_placeholders(template_content, results_dir, report_dir, assets_dir, experiment_name):
    """Replace placeholders in the template with actual data."""
    # Parse data
    benchmark_results = parse_benchmark_results(results_dir)
    metadata = parse_metadata(results_dir)
    perf_data = parse_perf_data(results_dir)
    assembly_files = find_assembly_files(results_dir)
    
    # Create tables and other formatted content
    benchmark_table = create_benchmark_table(benchmark_results)
    benchmark_console_output = add_benchmark_table_output(results_dir)
    metadata_table = create_metadata_table(metadata)
    assembly_links = create_assembly_links(assembly_files)
    
    # Start with the template content
    content = template_content
    
    # Replace Google Benchmark placeholders
    content = content.replace('{{GBENCH_TABLE}}', benchmark_table)
    content = content.replace('{{GBENCH_CONSOLE_OUTPUT}}', benchmark_console_output)
    if benchmark_results:
        content = content.replace('{{GBENCH_JSON}}', f"```json\n{json.dumps(benchmark_results, indent=2)}\n```")
    else:
        content = content.replace('{{GBENCH_JSON}}', "[No benchmark JSON available]")
    
    # Replace metadata placeholders
    content = content.replace('{{METADATA_TABLE}}', metadata_table)
    
    # Replace specific metadata field placeholders
    # Match patterns like {{METADATA:field.subfield}}
    for match in re.finditer(r'{{METADATA:([^}]+)}}', content):
        field_path = match.group(1)
        field_value = "Unknown"
        
        # Navigate nested fields using dot notation
        curr_obj = metadata
        for part in field_path.split('.'):
            if isinstance(curr_obj, dict) and part in curr_obj:
                curr_obj = curr_obj[part]
            else:
                curr_obj = "Unknown"
                break
        
        field_value = str(curr_obj)
        content = content.replace(match.group(0), field_value)
    
    # Replace perf data placeholders
    content = content.replace('{{PERF_SUMMARY}}', perf_data)
    content = content.replace('{{PERF_LOG}}', f"```\n{perf_data}\n```")
    
    # Replace assembly placeholders
    content = content.replace('{{ASSEMBLY_LINKS}}', assembly_links)
    
    # Replace specific assembly placeholders
    for func_name, asm_code in assembly_files.items():
        placeholder = f"{{{{ASSEMBLY:{func_name}}}}}"
        if placeholder in content:
            content = content.replace(placeholder, f"{asm_code}")
    
    # Handle assembly placeholders that weren't replaced
    for match in re.finditer(r'{{ASSEMBLY:([^}]+)}}', content):
        func_name = match.group(1)
        content = content.replace(match.group(0), f"[Assembly Snippet Not Found: {func_name}]")
    
    # Handle asset placeholders
    # Replace {{FIGURES:pattern}} with Markdown image links
    for match in re.finditer(r'{{FIGURES:([^}]+)}}', content):
        pattern = match.group(1)
        figures = find_assets(assets_dir, pattern)
        
        if figures:
            figure_links = ""
            for fig in figures:
                rel_path = fig.relative_to(report_dir)
                figure_links += f"![{fig.name}]({rel_path})\n\n"
            content = content.replace(match.group(0), figure_links.strip())
        else:
            content = content.replace(match.group(0), f"[No figures matching '{pattern}' found]")
    
    # Replace {{ASSETS:pattern}} with Markdown links
    for match in re.finditer(r'{{ASSETS:([^}]+)}}', content):
        pattern = match.group(1)
        assets = find_assets(assets_dir, pattern)
        
        if assets:
            asset_links = ""
            for asset in assets:
                rel_path = asset.relative_to(report_dir)
                asset_links += f"[{asset.name}]({rel_path})\n"
            content = content.replace(match.group(0), asset_links.strip())
        else:
            content = content.replace(match.group(0), f"[No assets matching '{pattern}' found]")
    
    # Replace {{FIGURE:filename}} with a specific Markdown image link
    for match in re.finditer(r'{{FIGURE:([^}]+)}}', content):
        filename = match.group(1)
        figure_path = assets_dir / filename
        
        if figure_path.exists():
            rel_path = figure_path.relative_to(report_dir)
            figure_link = f"![{filename}]({rel_path})"
            content = content.replace(match.group(0), figure_link)
        else:
            content = content.replace(match.group(0), f"[Figure Not Found: {filename}]")
    
    # Replace {{ASSET:filename}} with a specific Markdown link
    for match in re.finditer(r'{{ASSET:([^}]+)}}', content):
        filename = match.group(1)
        asset_path = assets_dir / filename
        
        if asset_path.exists():
            rel_path = asset_path.relative_to(report_dir)
            asset_link = f"[{filename}]({rel_path})"
            content = content.replace(match.group(0), asset_link)
        else:
            content = content.replace(match.group(0), f"[Asset Not Found: {filename}]")
    
    return content

def add_benchmark_table_output(results_dir):
    """Add the console/table output from Google Benchmark."""
    benchmark_table_file = results_dir / "benchmark_output.txt"
    if not benchmark_table_file.exists():
        return "**Console output not available.**"
    
    try:
        with open(benchmark_table_file, 'r') as f:
            console_output = f.read()
        
        # Format as a code block
        output = "### Console Output\n\n"
        output += "```\n"
        output += console_output
        output += "```\n"
        return output
    except Exception as e:
        logger.error(f"Error reading benchmark table file: {e}")
        return "**Error reading console output.**"

def generate_report(results_dir):
    """Generate a report from the given results directory."""
    results_dir = Path(results_dir) if not isinstance(results_dir, Path) else results_dir
    
    # Check if results directory exists
    if not results_dir.exists():
        logger.error(f"Results directory not found: {results_dir}")
        return False
    
    # Get experiment name from the results directory
    experiment_name = results_dir.name
    
    # Read metadata to confirm metadata_hash
    metadata_file = results_dir / "metadata.json"
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                if 'metadata_hash' in metadata:
                    # Verify that the metadata hash matches the directory name
                    if results_dir.parent.name != metadata['metadata_hash']:
                        logger.warning(f"Metadata hash in file ({metadata['metadata_hash']}) doesn't match directory name ({results_dir.parent.name})")
        except Exception as e:
            logger.warning(f"Could not verify metadata hash: {e}")
    
    # Create report directories
    report_dir, assets_dir, experiment_name = create_report_directories(results_dir)
    
    # Find template file
    template_path = find_template_file(experiment_name)
    if not template_path:
        logger.error(f"Template file not found for experiment: {experiment_name}")
        return False
    
    # Read template content
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except Exception as e:
        logger.error(f"Error reading template file: {e}")
        return False
    
    # Run pre-report script
    run_pre_report_script(experiment_name, results_dir, assets_dir)
    
    # Replace placeholders
    report_content = replace_placeholders(template_content, results_dir, report_dir, assets_dir, experiment_name)
    
    # Write report
    report_path = report_dir / "report.md"
    try:
        with open(report_path, 'w') as f:
            f.write(report_content)
        logger.info(f"Report generated successfully: {report_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing report: {e}")
        return False

def find_all_result_directories():
    """Find all available result directories in the results/ folder."""
    results_dirs = []
    
    # Pattern to match result directories with the expected structure
    # <results>/<platform>/<compiler>/<build_flags>/<metadata_hash>/<experiment>
    pattern = str(PROJECT_ROOT / "results" / "**" / "**" / "**" / "**" / "**")
    
    for path in glob.glob(pattern, recursive=True):
        path = Path(path)
        # Check if it's a directory and contains metadata.json (confirming it's a valid result directory)
        if path.is_dir() and (path / "metadata.json").exists():
            results_dirs.append(path)
    
    # remove duplicates
    results_dirs = list(set(results_dirs))
    
    return results_dirs

def main():
    """Main function to generate reports."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate a report from benchmark results')
    parser.add_argument('--result-dir', 
                        help='Path to the result directory. If not specified, reports will be generated for all available results')
    args = parser.parse_args()
    
    if args.result_dir:
        # Generate report for a specific result directory
        success = generate_report(args.result_dir)
        # Exit with appropriate status code
        sys.exit(0 if success else 1)
    else:
        # Generate reports for all available result directories
        logger.info("No specific result directory provided. Generating reports for all available results...")
        results_dirs = find_all_result_directories()
        
        if not results_dirs:
            logger.info("No result directories found. Make sure you have run benchmarks first.")
            sys.exit(1)
        
        # Track success status
        all_success = True
        successful_reports = 0
        failed_reports = 0
        
        for result_dir in results_dirs:
            logger.info(f"\nProcessing result directory: {result_dir}")
            try:
                success = generate_report(result_dir)
                if success:
                    successful_reports += 1
                else:
                    failed_reports += 1
                    all_success = False
            except Exception as e:
                logger.error(f"Error generating report for {result_dir}: {e}")
                failed_reports += 1
                all_success = False
        
        # Print summary
        logger.info(f"\nReport generation complete.")
        logger.info(f"Successfully generated reports: {successful_reports}")
        if failed_reports > 0:
            logger.info(f"Failed to generate reports: {failed_reports}")
        
        sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()