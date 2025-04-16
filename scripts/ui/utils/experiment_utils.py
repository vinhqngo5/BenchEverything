"""Utilities for experiment creation."""

import os
import json
from pathlib import Path

def create_experiment(exp_name, create_benchmark_cpp=True, update_cmake=True, update_config=True):
    """
    Create a new benchmark experiment with the given name.
    
    Args:
        exp_name (str): Name of the experiment to create
        create_benchmark_cpp (bool): Whether to create a benchmark.cpp file
        update_cmake (bool): Whether to update the main CMakeLists.txt
        update_config (bool): Whether to update benchmark_config.json
        
    Returns:
        list: List of messages indicating what was created/updated
    """
    messages = []
    
    # Create experiment directories
    exp_dir = Path('experiments') / exp_name
    src_dir = exp_dir / 'src'
    os.makedirs(src_dir, exist_ok=True)
    messages.append(f"Created directory structure for {exp_name}")
    
    # Prepare template variables
    title = exp_name.replace('_', ' ').title()
    function_name = exp_name.title().replace('_', '')
    description = exp_name.replace('_', ' ')
    
    # Create benchmark.cpp if needed
    if create_benchmark_cpp:
        benchmark_template = f"""#include <benchmark/benchmark.h>

// {title} benchmark
static void BM_{function_name}(benchmark::State& state) {{
  // Setup
  int a = 42;
  int b = 24;
  int result = 0;
  
  // Benchmark loop
  for (auto _ : state) {{
    // This is the operation we're benchmarking
    result = a + b;  // Replace with actual {description} operation
    
    // Prevent compiler from optimizing away the result
    benchmark::DoNotOptimize(result);
  }}
}}

// Register the benchmark function
BENCHMARK(BM_{function_name});

// Run the benchmark
BENCHMARK_MAIN();
"""
        with open(src_dir / 'benchmark.cpp', 'w') as f:
            f.write(benchmark_template)
        messages.append(f"Created benchmark.cpp for {exp_name}")
    
    # Create CMakeLists.txt
    cmake_template = f"""cmake_minimum_required(VERSION 3.15)

# Use our helper function to add this benchmark experiment
add_benchmark_experiment(
  NAME {exp_name}
  SRCS ${{CMAKE_CURRENT_SOURCE_DIR}}/src/benchmark.cpp
)
"""
    with open(exp_dir / 'CMakeLists.txt', 'w') as f:
        f.write(cmake_template)
    messages.append(f"Created CMakeLists.txt for {exp_name}")
    
    # Create README.md.template
    readme_template = f"""# {title} Benchmark

This benchmark measures the performance of {description} operations.

## Configuration

- Compiler: {{{{METADATA:compiler_version}}}}
- Flags: `{{{{METADATA:config.cxx_flags_used}}}}`
- Platform: {{{{METADATA:detailed_platform_id}}}}
- CPU: {{{{METADATA:cpu_model}}}}

## Benchmark Results

{{{{GBENCH_TABLE}}}}

{{{{GBENCH_CONSOLE_OUTPUT}}}}

## Assembly Code

```asm
{{{{ASSEMBLY:BM_{function_name}}}}}
```

## Performance Counters

{{{{PERF_SUMMARY}}}}

{{{{RELATED_LINKS}}}}
"""
    with open(exp_dir / 'README.md.template', 'w') as f:
        f.write(readme_template)
    messages.append(f"Created README.md.template for {exp_name}")
    
    # Update main CMakeLists.txt if needed
    if update_cmake:
        main_cmake = Path('CMakeLists.txt')
        if main_cmake.exists():
            with open(main_cmake, 'r') as f:
                content = f.read()
            if f'add_subdirectory(experiments/{exp_name})' not in content:
                with open(main_cmake, 'a') as f:
                    f.write(f'\nadd_subdirectory(experiments/{exp_name})\n')
                messages.append(f"Updated main CMakeLists.txt to include {exp_name}")
            else:
                messages.append(f"Main CMakeLists.txt already includes {exp_name}")
    
    # Update benchmark_config.json if needed
    if update_config:
        config_path = Path('scripts/config/benchmark_config.json')
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                # Check if experiment already exists
                exp_exists = False
                for exp in config.get('experiments', []):
                    if exp.get('name') == exp_name:
                        exp_exists = True
                        break
                        
                if not exp_exists:
                    config['experiments'].append({'name': exp_name})
                    
                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=2)
                    messages.append(f"Updated benchmark_config.json to include {exp_name}")
                else:
                    messages.append(f"Experiment {exp_name} already exists in benchmark_config.json")
            except Exception as e:
                messages.append(f"Error updating config: {e}")
    
    messages.append(f"Successfully created experiment: {exp_name}")
    return messages