"""Tab for creating new benchmark experiments."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QGroupBox, QCheckBox
)
from PySide6.QtCore import Signal


class CreateExperimentTab(QWidget):
    """Tab for creating new benchmark experiments."""
    
    command_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Experiment name input
        self.exp_name_input = QLineEdit()
        self.exp_name_input.textChanged.connect(self.update_command)
        form_layout.addRow("Experiment Name:", self.exp_name_input)
        
        # Template options
        self.template_group = QGroupBox("Template Options")
        template_layout = QVBoxLayout(self.template_group)
        
        self.create_benchmark_cpp = QCheckBox("Create basic benchmark.cpp")
        self.create_benchmark_cpp.setChecked(True)
        self.create_benchmark_cpp.stateChanged.connect(self.update_command)
        
        self.update_cmake = QCheckBox("Auto-update main CMakeLists.txt")
        self.update_cmake.setChecked(True)
        self.update_cmake.stateChanged.connect(self.update_command)
        
        self.update_config = QCheckBox("Auto-update benchmark_config.json")
        self.update_config.setChecked(True)
        self.update_config.stateChanged.connect(self.update_command)
        
        template_layout.addWidget(self.create_benchmark_cpp)
        template_layout.addWidget(self.update_cmake)
        template_layout.addWidget(self.update_config)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.template_group)
        layout.addStretch()
        
        self.update_command()
    
    def update_command(self):
        """Update the command preview based on current settings."""
        exp_name = self.exp_name_input.text().strip()
        if not exp_name:
            self.command_changed.emit("# Please enter an experiment name")
            return
        
        # This is a conceptual representation - in real implementation
        # we'd build a proper Python script to create experiments
        command = f"# Creating experiment: {exp_name}\n"
        
        # Add commands that would be executed
        command += f"mkdir -p experiments/{exp_name}/src\n"
        
        if self.create_benchmark_cpp.isChecked():
            command += f"# Creating experiments/{exp_name}/src/benchmark.cpp\n"
        
        command += f"# Creating experiments/{exp_name}/CMakeLists.txt\n"
        command += f"# Creating experiments/{exp_name}/README.md.template\n"
        
        if self.update_cmake.isChecked():
            command += f"# Updating root CMakeLists.txt\n"
        
        if self.update_config.isChecked():
            command += f"# Updating scripts/config/benchmark_config.json\n"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the actual command to execute."""
        exp_name = self.exp_name_input.text().strip()
        if not exp_name:
            return ""
        
        # Build a real Python command that creates the experiment with all required files
        cmd = f"""python -c \"
import os
import shutil
from pathlib import Path

# Create experiment directories
exp_dir = Path('experiments/{exp_name}')
src_dir = exp_dir / 'src'
os.makedirs(src_dir, exist_ok=True)

# Create benchmark.cpp
if {str(self.create_benchmark_cpp.isChecked()).lower()}:
    with open(src_dir / 'benchmark.cpp', 'w') as f:
        f.write('''#include <benchmark/benchmark.h>

// Simple benchmark function
static void BM_{exp_name}(benchmark::State& state) {{
    // Perform setup here
    
    for (auto _ : state) {{
        // This code gets timed
        benchmark::DoNotOptimize(0);
    }}
    
    // Teardown
}}

// Register the benchmark
BENCHMARK(BM_{exp_name});
BENCHMARK_MAIN();
''')

# Create CMakeLists.txt
with open(exp_dir / 'CMakeLists.txt', 'w') as f:
    f.write('''cmake_minimum_required(VERSION 3.15)

# Use our helper function to add this benchmark experiment
add_benchmark_experiment(
  NAME {exp_name}
  SRCS ${{CMAKE_CURRENT_SOURCE_DIR}}/src/benchmark.cpp
)
''')

# Create README.md.template
with open(exp_dir / 'README.md.template', 'w') as f:
    f.write('''# {exp_name.replace('_', ' ').title()} Benchmark

This benchmark measures the performance of {exp_name.replace('_', ' ')} operations.

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
{{{{ASSEMBLY:BM_{exp_name}}}}}
```

## Performance Counters

{{{{PERF_SUMMARY}}}}

{{{{RELATED_LINKS}}}}
''')

# Update main CMakeLists.txt if needed
if {str(self.update_cmake.isChecked()).lower()}:
    main_cmake = Path('CMakeLists.txt')
    if main_cmake.exists():
        with open(main_cmake, 'r') as f:
            content = f.read()
        if 'add_subdirectory(experiments/{exp_name})' not in content:
            with open(main_cmake, 'a') as f:
                f.write('\\nadd_subdirectory(experiments/{exp_name})\\n')
            print(f'Updated main CMakeLists.txt to include {exp_name}')

# Update benchmark_config.json if needed
if {str(self.update_config.isChecked()).lower()}:
    import json
    config_path = Path('scripts/config/benchmark_config.json')
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Check if experiment already exists
            exp_exists = False
            for exp in config.get('experiments', []):
                if exp.get('name') == '{exp_name}':
                    exp_exists = True
                    break
                    
            if not exp_exists:
                config['experiments'].append({{'name': '{exp_name}'}})
                
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f'Updated benchmark_config.json to include {exp_name}')
        except Exception as e:
            print(f'Error updating config: {{e}}')

print(f'Created experiment: {exp_name}')
\"
"""
        return cmd
    
    def clear_fields(self):
        """Clear all input fields."""
        self.exp_name_input.clear()
        self.create_benchmark_cpp.setChecked(True)
        self.update_cmake.setChecked(True)
        self.update_config.setChecked(True)