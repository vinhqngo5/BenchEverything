import math
import os
from pathlib import Path
from typing import Dict, Set, Optional, List

from .logger import get_logger

logger = get_logger()

# --- Markdown Table Generation ---

def create_gbench_table(benchmark_data: Dict) -> str:
    """Create a Markdown table from Google Benchmark JSON data."""
    if not benchmark_data or 'benchmarks' not in benchmark_data or not benchmark_data['benchmarks']:
        return "[No benchmark results available]"

    benchmarks = benchmark_data['benchmarks']
    first_benchmark = benchmarks[0]

    # Define columns to include and their display names
    column_mapping = {
        "name": "Benchmark",
        "real_time": "Time (ns)",
        "cpu_time": "CPU (ns)",
        "iterations": "Iterations",
        "items_per_second": "Items/s",
        "bytes_per_second": "Bytes/s",
        "time_unit": "Unit",
        "threads": "Threads",
        "repetitions": "Reps",
        "time_cv": "Time CV(%)",
        "cpu_cv": "CPU CV(%)",
        # Add more standard fields or user-defined fields if needed
    }

    # Determine columns present in the data, prioritize core ones
    core_columns = ["name", "real_time", "cpu_time", "iterations"]
    present_columns = {}

    # Add core columns if present
    for key in core_columns:
        if key in first_benchmark:
            present_columns[key] = column_mapping.get(key, key.replace('_', ' ').title())

    # Add other known/numeric columns if present
    for key, display_name in column_mapping.items():
         if key not in present_columns and key in first_benchmark:
              present_columns[key] = display_name

    # Add any other numeric/boolean fields not explicitly mapped (potential user metrics)
    excluded_fields = {
        "repetition_index", "family_index", "per_family_instance_index",
        "run_name", "run_type", "aggregate_name", "label", "error_occurred", "error_message"
    }
    for key, value in first_benchmark.items():
        if key not in present_columns and key not in excluded_fields:
             # Include if it looks like a metric (numeric, bool)
             if isinstance(value, (int, float, bool)) or \
                (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                 present_columns[key] = key.replace('_', ' ').title() # Default display name


    if not present_columns:
        return "[No benchmark metrics found]"

    # Create header
    header_titles = [present_columns[key] for key in present_columns]
    header_line = "| " + " | ".join(header_titles) + " |"
    separator_line = "| " + " | ".join(['-' * len(title) for title in header_titles]) + " |"
    table = header_line + "\n" + separator_line + "\n"

    # Create rows
    try:
        for benchmark in benchmarks:
            row = "| "
            for col_key in present_columns.keys():
                value = benchmark.get(col_key, "N/A")
                # Format numeric values (heuristic)
                is_integer_metric = col_key in ["iterations", "threads", "repetitions"]
                is_cv_metric = col_key in ["time_cv", "cpu_cv"]

                if isinstance(value, (int, float)) and not is_integer_metric:
                     precision = 2 if not is_cv_metric else 4 # More precision for CV
                     row += f"{value:.{precision}f} | "
                else:
                    row += f"{value} | "
            table += row.strip() + "\n" # Remove trailing space before newline
    except Exception as e:
        logger.error(f"Error creating benchmark table rows: {e}")
        return "[Error creating benchmark table]"

    return table


def create_metadata_table(metadata: Dict) -> str:
    """Create a Markdown table for key metadata fields."""
    if not metadata:
        return "[No metadata available]"

    table = "| Property           | Value |\n"
    table += "|--------------------|-------|\n"

    # Define key properties to display
    key_properties = [
        ("Experiment Name", "experiment_name"),
        ("Timestamp", "timestamp_iso"),
        ("Platform (Detailed)", "detailed_platform_id"),
        ("Compiler (Detailed)", "detailed_compiler_id"),
        ("Build Flags", "build_flags_id"),
        ("Metadata Hash", "metadata_hash"),
        ("CPU Model", "cpu_model"),
        ("Compiler Type", "compiler_type"), # Detected
        ("Compiler Version", "compiler_version"), # Detected
        ("CMake Build Type", "config.cmake_build_type"),
        ("CXX Flags Used", "config.cxx_flags_used"),
        # ("Metadata Source", "metadata_source"), # Can be long
    ]

    for display_name, key_path in key_properties:
        value = metadata
        try:
            for part in key_path.split('.'):
                 if isinstance(value, dict):
                      value = value.get(part, "N/A")
                 else:
                      value = "N/A"
                      break
        except Exception:
             value = "Error"

        # Handle potential long values
        value_str = str(value)
        if len(value_str) > 80: # Truncate long values
            value_str = value_str[:77] + "..."

        table += f"| {display_name:<18} | {value_str} |\n"

    return table

def create_assembly_links_section(assembly_files: Dict[str, Path], report_dir: Path) -> str:
    """Create Markdown links to assembly files, relative to the report."""
    if not assembly_files:
        return "No assembly files available."

    links = "### Assembly Files\n\n"
    # Sort by function name
    sorted_funcs = sorted(assembly_files.keys())

    for func_name in sorted_funcs:
        asm_path = assembly_files[func_name]
        try:
             # Make path relative to the report file's directory
             relative_path = os.path.relpath(asm_path, report_dir)
             # Ensure forward slashes for Markdown compatibility
             relative_path_md = relative_path.replace(os.sep, '/')
             links += f"- [{func_name}]({relative_path_md})\n"
        except ValueError:
             # Handle cases where paths are on different drives (Windows)
             links += f"- {func_name} (Path: {asm_path}) \n" # Fallback to absolute path
        except Exception as e:
             logger.error(f"Error creating relative path for assembly {asm_path}: {e}")
             links += f"- {func_name} (Error creating link)\n"


    return links


# --- Comparison Report Utilities ---

def identify_common_metrics(baseline_data: Dict, contender_data: Dict) -> Set[str]:
    """Identify metrics (numeric/bool) present in both benchmark datasets."""
    if not baseline_data or 'benchmarks' not in baseline_data or not baseline_data['benchmarks'] or \
       not contender_data or 'benchmarks' not in contender_data or not contender_data['benchmarks']:
        return set()

    # Metrics to exclude from comparison table (usually identifiers or non-numeric)
    excluded_fields = {
        "repetition_index", "family_index", "per_family_instance_index",
        "run_name", "run_type", "aggregate_name", "label", "time_unit", # time_unit handled separately if needed
        "error_occurred", "error_message"
    }

    def get_potential_metrics(data):
        metrics = set()
        first_benchmark = data['benchmarks'][0]
        for key, value in first_benchmark.items():
            if key not in excluded_fields:
                # Check if it looks like a numeric metric
                if isinstance(value, (int, float, bool)) or \
                   (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                    metrics.add(key)
        return metrics

    baseline_metrics = get_potential_metrics(baseline_data)
    contender_metrics = get_potential_metrics(contender_data)

    common = baseline_metrics.intersection(contender_metrics)
    logger.debug(f"Identified common metrics: {common}")
    return common

def calculate_improvement(baseline_value: float, contender_value: float, metric_name: str) -> float:
    """
    Calculate improvement percentage.
    Positive = contender is better. Negative = baseline is better.
    Handles division by zero.
    """
    # Metrics where lower is better
    lower_is_better = ['real_time', 'cpu_time', 'time', 'cycles', 'instructions', 'cache_misses']
    # Metrics where higher is better
    # higher_is_better = ['items_per_second', 'bytes_per_second'] # Add others as needed

    if baseline_value == 0:
        if contender_value == 0:
            return 0.0 # No change
        elif contender_value < 0 and metric_name in lower_is_better:
             return float('inf') # Baseline was zero, contender negative (inf improvement)
        elif contender_value > 0 and metric_name in lower_is_better:
             return float('-inf') # Baseline was zero, contender positive (inf regression)
        elif contender_value > 0: # Higher is better case
             return float('inf')
        else: # Contender < 0 for higher_is_better
             return float('-inf')

    # Normal calculation
    if metric_name in lower_is_better:
        improvement = ((baseline_value - contender_value) / abs(baseline_value)) * 100
    else: # Assume higher is better for all other numeric metrics
        improvement = ((contender_value - baseline_value) / abs(baseline_value)) * 100

    return improvement

def get_winner(improvement: float, threshold: float = 1.0) -> str:
    """Determine winner based on improvement percentage and threshold."""
    if abs(improvement) < threshold:
        return 'tie'
    return 'contender' if improvement > 0 else 'baseline'


def format_comparison_value(value):
     """Format numeric values for the comparison table."""
     if isinstance(value, (int, float)):
          # Use reasonable precision, avoid excessive decimals unless value is small
          if abs(value) > 10:
              return f"{value:.2f}"
          elif abs(value) > 0.01:
               return f"{value:.3f}"
          else:
                return f"{value:.4g}" # Use general format for very small numbers
     else:
          return str(value)

def format_improvement_value(improvement: float) -> str:
     """Format improvement percentage with color."""
     if not math.isfinite(improvement):
          color = "orange" # Indicate infinity
          value = "∞" if improvement > 0 else "-∞"
     elif improvement > 0.1: # Use 0.1% threshold for coloring
         color = "green"
         value = f"{improvement:.2f}%"
     elif improvement < -0.1:
         color = "red"
         value = f"{improvement:.2f}%"
     else: # Close to zero
         color = "grey"
         value = f"{improvement:.2f}%"

     return f"<span style='color:{color}'>{value}</span>"

def create_comparison_table(
    baseline_data: Dict, contender_data: Dict,
    baseline_label: str, contender_label: str,
    common_metrics: Set[str]
) -> str:
    """Create a Markdown comparison table."""
    if not baseline_data or 'benchmarks' not in baseline_data or \
       not contender_data or 'benchmarks' not in contender_data or not common_metrics:
        return "[No comparable benchmark data available]"

    # Metric display names and order
    metric_display_map = {
        'real_time': 'Time', 'cpu_time': 'CPU', 'iterations': 'Iters',
        'items_per_second': 'Items/s', 'bytes_per_second': 'Bytes/s',
        # Add more mappings as needed
    }
    core_metrics = ['real_time', 'cpu_time', 'iterations', 'items_per_second', 'bytes_per_second']

    ordered_metrics = [m for m in core_metrics if m in common_metrics]
    ordered_metrics.extend(sorted([m for m in common_metrics if m not in core_metrics]))

    if not ordered_metrics:
         return "[No common metrics found for comparison]"

    # Create headers
    headers = ['Benchmark']
    for metric in ordered_metrics:
        display_name = metric_display_map.get(metric, metric.replace('_', ' ').title())
        headers.append(f"{baseline_label} {display_name}")
        headers.append(f"{contender_label} {display_name}")
        headers.append(f"Improv.")
    headers.append("Winner")

    # Header rows
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["-" * len(h) for h in headers]) + " |\n"

    # Data rows
    baseline_benchmarks = {b['name']: b for b in baseline_data.get('benchmarks', [])}
    contender_benchmarks = {b['name']: b for b in contender_data.get('benchmarks', [])}
    common_benchmark_names = sorted(set(baseline_benchmarks.keys()).intersection(contender_benchmarks.keys()))

    if not common_benchmark_names:
         return "[No common benchmarks found between runs]"

    primary_metric = 'real_time' if 'real_time' in common_metrics else ('cpu_time' if 'cpu_time' in common_metrics else None)
    significant_diff_found = False

    for bench_name in common_benchmark_names:
        baseline_bench = baseline_benchmarks[bench_name]
        contender_bench = contender_benchmarks[bench_name]

        row_values = [bench_name]
        primary_improvement = 0.0

        for metric in ordered_metrics:
            try:
                b_val = baseline_bench.get(metric)
                c_val = contender_bench.get(metric)

                # Ensure values are numeric for calculation
                b_float = float(b_val)
                c_float = float(c_val)

                improvement = calculate_improvement(b_float, c_float, metric)

                row_values.append(format_comparison_value(b_val))
                row_values.append(format_comparison_value(c_val))
                row_values.append(format_improvement_value(improvement))

                if metric == primary_metric:
                    primary_improvement = improvement if math.isfinite(improvement) else (1e9 if improvement > 0 else -1e9)
                if abs(improvement) > 1.0 and math.isfinite(improvement): # Check for >1% diff
                     significant_diff_found = True

            except (ValueError, TypeError, KeyError) as e:
                logger.debug(f"Skipping metric '{metric}' for benchmark '{bench_name}' due to non-numeric value or missing key: {e}")
                row_values.append(str(baseline_bench.get(metric, "N/A")))
                row_values.append(str(contender_bench.get(metric, "N/A")))
                row_values.append("N/A") # Cannot calculate improvement

        # Determine winner based on primary metric
        winner = get_winner(primary_improvement)
        # Adjust winner label for clarity
        winner_label = contender_label if winner == 'contender' else (baseline_label if winner == 'baseline' else 'tie')
        row_values.append(winner_label)

        table += "| " + " | ".join(row_values) + " |\n"

    # Add note if no significant differences were found
    if not significant_diff_found:
         table += "\n*Note: No significant performance differences (> 1%) detected based on calculated improvements.*"

    # Check for differing configurations (iterations/repetitions)
    warnings = []
    for key in ['iterations', 'repetitions']:
        if key in common_metrics:
            baseline_vals = set(str(b.get(key)) for b in baseline_benchmarks.values() if key in b)
            contender_vals = set(str(b.get(key)) for b in contender_benchmarks.values() if key in b)
            if len(baseline_vals) > 1 or len(contender_vals) > 1 or baseline_vals != contender_vals:
                 warnings.append(f"**{key.capitalize()} differ:** Baseline: {sorted(list(baseline_vals))}, Contender: {sorted(list(contender_vals))}")

    if warnings:
        table += "\n**Configuration Warnings:** Google Benchmark determined different workloads, which may affect comparison quality:\n"
        for warning in warnings:
            table += f"- {warning}\n"

    return table


def create_metadata_comparison_table(baseline_metadata: Dict, contender_metadata: Dict) -> str:
    """Create a Markdown table comparing key metadata fields."""
    if not baseline_metadata or not contender_metadata:
        return "[Metadata comparison not available]"

    table = "| Property           | Baseline                     | Contender                    |\n"
    table += "|--------------------|------------------------------|------------------------------|\n"

    # Key properties to compare
    key_properties = [
        ("Platform (Detailed)", "detailed_platform_id"),
        ("Compiler (Detailed)", "detailed_compiler_id"),
        ("Build Flags", "build_flags_id"),
        ("Metadata Hash", "metadata_hash"),
        ("CPU Model", "cpu_model"),
        ("CMake Build Type", "config.cmake_build_type"),
        ("CXX Flags Used", "config.cxx_flags_used"),
        ("Timestamp", "timestamp_iso"),
    ]

    def get_value(metadata, key_path):
        value = metadata
        try:
            for part in key_path.split('.'):
                 if isinstance(value, dict):
                      value = value.get(part, "N/A")
                 else:
                      value = "N/A"; break
        except Exception: value = "Error"
        return str(value)

    for display_name, key_path in key_properties:
        b_val = get_value(baseline_metadata, key_path)
        c_val = get_value(contender_metadata, key_path)

        # Highlight differences
        b_val_disp = f"**{b_val}**" if b_val != c_val else b_val
        c_val_disp = f"**{c_val}**" if b_val != c_val else c_val

        # Limit length for table formatting
        max_len = 28
        b_val_disp = b_val_disp[:max_len] + "..." if len(b_val_disp) > max_len else b_val_disp
        c_val_disp = c_val_disp[:max_len] + "..." if len(c_val_disp) > max_len else c_val_disp

        table += f"| {display_name:<18} | {b_val_disp:<28} | {c_val_disp:<28} |\n"

    return table

# --- Path Formatting ---

def format_path_for_markdown(target_path: Path, report_dir: Path, project_root: Path) -> str:
    """
    Create a relative path suitable for Markdown links from the report directory.
    Handles paths inside and outside the project root.
    """
    try:
        # Ensure target_path is absolute
        if not target_path.is_absolute():
             target_path = (project_root / target_path).resolve()

        # Calculate path relative to the *directory containing the report*
        relative_path = os.path.relpath(target_path, report_dir)
        # Convert to forward slashes for Markdown/URL compatibility
        markdown_path = relative_path.replace(os.sep, '/')
        return markdown_path
    except ValueError:
        # Paths might be on different drives (Windows) or other errors
        logger.warning(f"Could not create relative path from {report_dir} to {target_path}. Using absolute URI.")
        return target_path.as_uri() # Fallback to file URI
    except Exception as e:
        logger.error(f"Error formatting path {target_path} relative to {report_dir}: {e}")
        return str(target_path) # Fallback to string representation


def get_configuration_label(metadata: Optional[Dict], fallback_name: str = "Unknown") -> str:
    """Generate a concise, user-friendly label for a configuration run."""
    if not metadata:
        return fallback_name

    compiler_id = metadata.get('detailed_compiler_id', 'unknown-compiler')
    build_flags = metadata.get('build_flags_id', 'unknown-flags')

    # Extract compiler name/version roughly
    parts = compiler_id.split('-', 1)
    compiler_name = parts[0]
    compiler_version = parts[1] if len(parts) > 1 else ""

    # Combine, e.g., "clang-15.0.0 (Release_O3)"
    label = f"{compiler_name}"
    if compiler_version and compiler_version != "unknown_version":
        label += f" {compiler_version.split('.')[0]}" # Just major version? or full? Let's try full for now.
        # label += f" {compiler_version}"
    label += f" ({build_flags})"

    return label.replace('_', ' ') # Replace underscore in flags for readability

def get_results_dir_path_from_metadata(metadata: Dict, project_root: Path) -> Optional[Path]:
     """Reconstruct the results directory path from metadata fields."""
     try:
          platform = metadata['detailed_platform_id']
          compiler = metadata['detailed_compiler_id']
          flags = metadata['build_flags_id']
          mhash = metadata['metadata_hash']
          exp_name = metadata['experiment_name']
          return project_root / "results" / platform / compiler / flags / mhash / exp_name
     except KeyError as e:
          logger.error(f"Metadata missing required key to reconstruct path: {e}")
          return None

def get_report_path_from_metadata(metadata: Dict, project_root: Path) -> Optional[Path]:
    """Reconstruct the report.md path from metadata fields."""
    try:
        platform = metadata['detailed_platform_id']
        compiler = metadata['detailed_compiler_id']
        flags = metadata['build_flags_id']
        mhash = metadata['metadata_hash']
        exp_name = metadata['experiment_name']
        return project_root / "reports" / platform / compiler / flags / mhash / exp_name / "report.md"
    except KeyError as e:
         logger.error(f"Metadata missing required key to reconstruct report path: {e}")
         return None