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
from pathlib import Path
from datetime import datetime

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
            print(f"Running pre-report script: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"Pre-report script completed successfully")
            return True
        except subprocess.SubprocessError as e:
            print(f"Warning: Pre-report script failed: {e}")
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
        print(f"Error parsing results directory: {e}")
    
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
        print(f"Error creating report directories: {e}")
        sys.exit(1)

def parse_benchmark_results(results_dir):
    """Parse Google Benchmark results from benchmark_output.json."""
    benchmark_file = results_dir / "benchmark_output.json"
    if not benchmark_file.exists():
        print(f"Error: Benchmark results file not found: {benchmark_file}")
        return None
    
    try:
        with open(benchmark_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing benchmark results: {e}")
        return None

def parse_metadata(results_dir):
    """Parse metadata from metadata.json."""
    metadata_file = results_dir / "metadata.json"
    if not metadata_file.exists():
        print(f"Warning: Metadata file not found: {metadata_file}")
        return {}
    
    try:
        with open(metadata_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing metadata: {e}")
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
        print(f"Error parsing perf data: {e}")
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
            print(f"Error reading assembly file {asm_file}: {e}")
            assembly_files[func_name] = f"Error reading assembly for {func_name}"
    
    return assembly_files

def create_benchmark_table(benchmark_results):
    """Create a Markdown table from benchmark results."""
    if not benchmark_results:
        return "[No benchmark results available]"
    
    table = "| Benchmark | Time (ns) | CPU (ns) | Iterations |\n"
    table += "|-----------|----------|---------|------------|\n"
    
    try:
        for benchmark in benchmark_results.get('benchmarks', []):
            name = benchmark.get('name', 'Unknown')
            time = benchmark.get('real_time', 0)
            cpu = benchmark.get('cpu_time', 0)
            iterations = benchmark.get('iterations', 0)
            
            table += f"| {name} | {time:.2f} | {cpu:.2f} | {iterations} |\n"
    except Exception as e:
        print(f"Error creating benchmark table: {e}")
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
        print(f"Error creating metadata table: {e}")
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
    metadata_table = create_metadata_table(metadata)
    assembly_links = create_assembly_links(assembly_files)
    
    # Start with the template content
    content = template_content
    
    # Replace Google Benchmark placeholders
    content = content.replace('{{GBENCH_TABLE}}', benchmark_table)
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
            content = content.replace(placeholder, asm_code)
    
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

def generate_report(results_dir):
    """Generate a report from the given results directory."""
    results_dir = Path(results_dir) if not isinstance(results_dir, Path) else results_dir
    
    # Check if results directory exists
    if not results_dir.exists():
        print(f"Error: Results directory not found: {results_dir}")
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
                        print(f"Warning: Metadata hash in file ({metadata['metadata_hash']}) doesn't match directory name ({results_dir.parent.name})")
        except Exception as e:
            print(f"Warning: Could not verify metadata hash: {e}")
    
    # Create report directories
    report_dir, assets_dir, experiment_name = create_report_directories(results_dir)
    
    # Find template file
    template_path = find_template_file(experiment_name)
    if not template_path:
        print(f"Error: Template file not found for experiment: {experiment_name}")
        return False
    
    # Read template content
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
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
        print(f"Report generated successfully: {report_path}")
        return True
    except Exception as e:
        print(f"Error writing report: {e}")
        return False

def main():
    """Main function to generate reports."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate a report from benchmark results')
    parser.add_argument('--result-dir', required=True,
                        help='Path to the result directory')
    args = parser.parse_args()
    
    # Generate report
    success = generate_report(args.result_dir)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()