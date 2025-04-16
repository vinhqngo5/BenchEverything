#!/usr/bin/env python3

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QTextEdit, QLabel, QSplitter, QFileDialog, QMessageBox,
        QCheckBox, QComboBox, QListWidget, QListWidgetItem, QLineEdit, QGroupBox, QRadioButton,
        QFormLayout, QScrollArea
    )
    from PySide6.QtCore import Qt, QThread, Signal, Slot, QProcess, QSize
    from PySide6.QtGui import QFont, QTextCursor, QIcon
except ImportError:
    print("Error: PySide6 is required. Please install it with 'pip install PySide6'")
    sys.exit(1)

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class CommandThread(QThread):
    """Thread for executing commands without blocking the UI."""
    output_received = Signal(str)
    error_received = Signal(str)
    command_finished = Signal(int)
    
    def __init__(self, command: str):
        super().__init__()
        self.command = command
        self.process = None
        self.stopped = False
    
    def run(self):
        """Execute the command and process its output."""
        try:
            # Start the process
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                shell=True
            )
            
            # Read stdout
            for line in iter(self.process.stdout.readline, ''):
                if self.stopped:
                    break
                self.output_received.emit(line.rstrip())
            
            # Read stderr
            for line in iter(self.process.stderr.readline, ''):
                if self.stopped:
                    break
                self.error_received.emit(line.rstrip())
            
            # Wait for process to complete
            exit_code = self.process.wait()
            if not self.stopped:
                self.command_finished.emit(exit_code)
        
        except Exception as e:
            self.error_received.emit(f"Error running command: {str(e)}")
            self.command_finished.emit(1)
    
    def stop(self):
        """Stop the running command."""
        if self.process and self.process.poll() is None:
            self.stopped = True
            self.process.terminate()
            self.process.wait(timeout=3)
            # Force kill if not terminated after timeout
            if self.process.poll() is None:
                self.process.kill()


class PathSelector(QWidget):
    """Custom widget for selecting file/directory paths."""
    
    path_changed = Signal(str)
    
    def __init__(self, parent=None, dialog_type="dir", dialog_caption="Select Path", 
                 file_filter="All Files (*)"):
        super().__init__(parent)
        self.dialog_type = dialog_type  # "dir" or "file"
        self.dialog_caption = dialog_caption
        self.file_filter = file_filter
        
        # Set up layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Path input field
        self.path_input = QLineEdit()
        self.path_input.textChanged.connect(self.on_path_changed)
        layout.addWidget(self.path_input)
        
        # Browse button
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.on_browse_clicked)
        layout.addWidget(self.browse_button)
    
    def on_browse_clicked(self):
        """Open file/directory selection dialog."""
        current_path = self.path_input.text()
        start_dir = current_path if os.path.exists(current_path) else str(PROJECT_ROOT)
        
        if self.dialog_type == "dir":
            path = QFileDialog.getExistingDirectory(
                self, self.dialog_caption, start_dir
            )
        else:  # file
            path, _ = QFileDialog.getOpenFileName(
                self, self.dialog_caption, start_dir, self.file_filter
            )
        
        if path:
            self.path_input.setText(path)
    
    def on_path_changed(self, path):
        """Emit signal when path changes."""
        self.path_changed.emit(path)
    
    def get_path(self) -> str:
        """Get the current path."""
        return self.path_input.text()
    
    def set_path(self, path: str):
        """Set the current path."""
        self.path_input.setText(path)


class CommonControls(QWidget):
    """Widget containing common controls shared across all tabs."""
    
    run_clicked = Signal()
    stop_clicked = Signal()
    clear_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Command preview section
        preview_group = QGroupBox("Command Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setMaximumHeight(80)
        preview_layout.addWidget(self.command_preview)
        
        layout.addWidget(preview_group)
        
        # Output console section
        output_group = QGroupBox("Output Console")
        output_layout = QVBoxLayout(output_group)
        
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Monospace"))
        self.output_console.setMinimumHeight(200)
        output_layout.addWidget(self.output_console)
        
        layout.addWidget(output_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear Output")
        self.clear_button.clicked.connect(self.clear_clicked)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_clicked)
        self.stop_button.setEnabled(False)  # Initially disabled
        
        self.run_button = QPushButton("Run Command")
        self.run_button.clicked.connect(self.run_clicked)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.run_button)
        
        layout.addLayout(button_layout)
    
    def set_command_preview(self, command: str):
        """Update the command preview text."""
        self.command_preview.setText(command)
    
    def append_output(self, text: str, is_error: bool = False):
        """Append text to the output console."""
        cursor = self.output_console.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Apply different formatting for errors if needed
        if is_error:
            format_html = f"<span style='color: red;'>{text}</span><br>"
        else:
            format_html = f"{text}<br>"
        
        cursor.insertHtml(format_html)
        self.output_console.setTextCursor(cursor)
        self.output_console.ensureCursorVisible()
    
    def clear_output(self):
        """Clear the output console."""
        self.output_console.clear()
    
    def set_running_state(self, is_running: bool):
        """Update the UI for running/stopped state."""
        self.run_button.setEnabled(not is_running)
        self.stop_button.setEnabled(is_running)


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


class RunBenchmarksTab(QWidget):
    """Tab for running benchmark experiments."""
    
    command_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Config path selection (moved to top)
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Config File:"))
        
        self.config_path = PathSelector(dialog_type="file", dialog_caption="Select Config File", 
                                       file_filter="JSON Files (*.json)")
        # Connect load_config_from_path first
        self.config_path.path_changed.connect(self.load_config_from_path) 
        
        config_layout.addWidget(self.config_path)
        layout.addLayout(config_layout)
        
        # Experiment selection
        self.exp_group = QGroupBox("Experiment Selection")
        exp_layout = QVBoxLayout(self.exp_group)
        
        self.exp_list = QListWidget()
        self.exp_list.setSelectionMode(QListWidget.MultiSelection)
        
        exp_buttons_layout = QHBoxLayout()
        self.select_all_exp = QPushButton("Select All")
        self.select_all_exp.clicked.connect(self.select_all_experiments)
        self.select_none_exp = QPushButton("Select None")
        self.select_none_exp.clicked.connect(self.select_no_experiments)
        
        exp_buttons_layout.addWidget(self.select_all_exp)
        exp_buttons_layout.addWidget(self.select_none_exp)
        
        exp_layout.addLayout(exp_buttons_layout)
        exp_layout.addWidget(self.exp_list)
        
        layout.addWidget(self.exp_group)
        
        # Compiler selection
        self.compiler_group = QGroupBox("Compiler Selection")
        compiler_layout = QVBoxLayout(self.compiler_group)
        
        self.compiler_list = QListWidget()
        self.compiler_list.setSelectionMode(QListWidget.MultiSelection)
        
        compiler_buttons_layout = QHBoxLayout()
        self.select_all_compiler = QPushButton("Select All")
        self.select_all_compiler.clicked.connect(self.select_all_compilers)
        self.select_none_compiler = QPushButton("Select None")
        self.select_none_compiler.clicked.connect(self.select_no_compilers)
        
        compiler_buttons_layout.addWidget(self.select_all_compiler)
        compiler_buttons_layout.addWidget(self.select_none_compiler)
        
        compiler_layout.addLayout(compiler_buttons_layout)
        compiler_layout.addWidget(self.compiler_list)
        
        layout.addWidget(self.compiler_group)
        
        # Build flags
        flags_layout = QHBoxLayout()
        flags_layout.addWidget(QLabel("Build Flags:"))
        
        self.build_flags = QComboBox()
        self.build_flags.setEditable(True)
        self.build_flags.addItems([
            "Release_O3", "Debug_O0", "RelWithDebInfo_O2"
        ])
        
        flags_layout.addWidget(self.build_flags)
        layout.addLayout(flags_layout)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.force_rerun = QCheckBox("Force Re-run")
        options_layout.addWidget(self.force_rerun)
        
        self.incremental_build = QCheckBox("Incremental Build")
        options_layout.addWidget(self.incremental_build)
        
        layout.addLayout(options_layout)
        
        # Additional options (collapsible)
        self.advanced_group = QGroupBox("Additional Options")
        self.advanced_group.setCheckable(True)
        self.advanced_group.setChecked(False)
        
        advanced_layout = QVBoxLayout(self.advanced_group)
        
        self.extra_flags = QLineEdit()
        self.extra_flags.setPlaceholderText("Extra flags for run_benchmarks.py")
        
        advanced_layout.addWidget(self.extra_flags)
        
        layout.addWidget(self.advanced_group)
        layout.addStretch()
        
        # Load config immediately from default path
        default_config_path = str(PROJECT_ROOT / "scripts" / "config" / "benchmark_config.json")
        self.config_path.set_path(default_config_path) # This might trigger load_config_from_path
        
        # Connect signals that trigger update_command *after* all widgets are created
        self.config_path.path_changed.connect(self.update_command)
        self.exp_list.itemSelectionChanged.connect(self.update_command)
        self.compiler_list.itemSelectionChanged.connect(self.update_command)
        self.build_flags.currentTextChanged.connect(self.update_command)
        self.force_rerun.stateChanged.connect(self.update_command)
        self.incremental_build.stateChanged.connect(self.update_command)
        self.advanced_group.toggled.connect(self.update_command)
        self.extra_flags.textChanged.connect(self.update_command)

        # If load_config_from_path wasn't triggered by set_path, load manually
        if self.exp_list.count() == 0: 
            self.load_config() 
            
        # Perform initial command update
        self.update_command()
    
    def load_config(self):
        """Load configuration from benchmark_config.json."""
        try:
            config_path = PROJECT_ROOT / "scripts" / "config" / "benchmark_config.json"
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Populate experiment list
            self.exp_list.clear()
            for exp in config.get('experiments', []):
                if 'name' in exp:
                    self.exp_list.addItem(exp['name'])
            
            # Populate compiler list
            self.compiler_list.clear()
            for compiler in config.get('compilers', []):
                if 'name' in compiler:
                    self.compiler_list.addItem(compiler['name'])
            
            # Select the first items by default
            if self.exp_list.count() > 0:
                self.exp_list.item(0).setSelected(True)
            
            if self.compiler_list.count() > 0:
                self.compiler_list.item(0).setSelected(True)
        
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def load_config_from_path(self, path):
        """Load configuration from a specified path."""
        try:
            with open(path, 'r') as f:
                config = json.load(f)
            
            # Populate experiment list
            self.exp_list.clear()
            for exp in config.get('experiments', []):
                if 'name' in exp:
                    self.exp_list.addItem(exp['name'])
            
            # Populate compiler list
            self.compiler_list.clear()
            for compiler in config.get('compilers', []):
                if 'name' in compiler:
                    self.compiler_list.addItem(compiler['name'])
            
            # Select the first items by default
            if self.exp_list.count() > 0:
                self.exp_list.item(0).setSelected(True)
            
            if self.compiler_list.count() > 0:
                self.compiler_list.item(0).setSelected(True)
        
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def select_all_experiments(self):
        """Select all experiments in the list."""
        for i in range(self.exp_list.count()):
            self.exp_list.item(i).setSelected(True)
        self.update_command()
    
    def select_no_experiments(self):
        """Deselect all experiments in the list."""
        for i in range(self.exp_list.count()):
            self.exp_list.item(i).setSelected(False)
        self.update_command()
    
    def select_all_compilers(self):
        """Select all compilers in the list."""
        for i in range(self.compiler_list.count()):
            self.compiler_list.item(i).setSelected(True)
        self.update_command()
    
    def select_no_compilers(self):
        """Deselect all compilers in the list."""
        for i in range(self.compiler_list.count()):
            self.compiler_list.item(i).setSelected(False)
        self.update_command()
    
    def update_command(self):
        """Update the command preview based on current settings."""
        command = "python scripts/run_benchmarks.py"
        
        # Add experiments
        selected_experiments = []
        for i in range(self.exp_list.count()):
            if self.exp_list.item(i).isSelected():
                selected_experiments.append(self.exp_list.item(i).text())
        
        if selected_experiments:
            command += f" --experiments {','.join(selected_experiments)}"
        
        # Add compilers
        selected_compilers = []
        for i in range(self.compiler_list.count()):
            if self.compiler_list.item(i).isSelected():
                selected_compilers.append(self.compiler_list.item(i).text())
        
        if selected_compilers:
            command += f" --compiler {','.join(selected_compilers)}"
        
        # Add build flags
        build_flags = self.build_flags.currentText()
        if build_flags:
            command += f" --build-flags {build_flags}"
        
        # Add options
        if self.force_rerun.isChecked():
            command += " --force"
        
        if self.incremental_build.isChecked():
            command += " --incremental-build"
        
        # Add custom config
        config_path = self.config_path.get_path()
        if config_path:
            command += f" --config {config_path}"
        
        # Add extra flags
        if self.advanced_group.isChecked():
            extra_flags = self.extra_flags.text()
            if extra_flags:
                command += f" {extra_flags}"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the command to execute."""
        command = "python scripts/run_benchmarks.py"
        
        # Add experiments
        selected_experiments = []
        for i in range(self.exp_list.count()):
            if self.exp_list.item(i).isSelected():
                selected_experiments.append(self.exp_list.item(i).text())
        
        if selected_experiments:
            command += f" --experiments {','.join(selected_experiments)}"
        
        # Add compilers
        selected_compilers = []
        for i in range(self.compiler_list.count()):
            if self.compiler_list.item(i).isSelected():
                selected_compilers.append(self.compiler_list.item(i).text())
        
        if selected_compilers:
            command += f" --compiler {','.join(selected_compilers)}"
        
        # Add build flags
        build_flags = self.build_flags.currentText()
        if build_flags:
            command += f" --build-flags {build_flags}"
        
        # Add options
        if self.force_rerun.isChecked():
            command += " --force"
        
        if self.incremental_build.isChecked():
            command += " --incremental-build"
        
        # Add custom config
        config_path = self.config_path.get_path()
        if config_path:
            command += f" --config {config_path}"
        
        # Add extra flags
        if self.advanced_group.isChecked():
            extra_flags = self.extra_flags.text()
            if extra_flags:
                command += f" {extra_flags}"
        
        return command


class GenerateReportTab(QWidget):
    """Tab for generating reports from benchmark results."""
    
    command_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Result directory selection
        result_layout = QVBoxLayout()
        
        self.all_results = QCheckBox("Generate reports for all results")
        self.all_results.stateChanged.connect(self.toggle_result_selector)
        self.all_results.stateChanged.connect(self.update_command)
        result_layout.addWidget(self.all_results)
        
        result_dir_layout = QHBoxLayout()
        result_dir_layout.addWidget(QLabel("Result Directory:"))
        
        self.result_dir = PathSelector(dialog_type="dir", dialog_caption="Select Result Directory")
        self.result_dir.path_changed.connect(self.update_command)
        result_dir_layout.addWidget(self.result_dir)
        
        result_layout.addLayout(result_dir_layout)
        layout.addLayout(result_layout)
        
        # Output options
        self.output_group = QGroupBox("Output Options")
        output_layout = QVBoxLayout(self.output_group)
        
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(QLabel("Custom Output Directory:"))
        
        self.output_dir = PathSelector(dialog_type="dir", dialog_caption="Select Output Directory")
        self.output_dir.path_changed.connect(self.update_command)
        output_dir_layout.addWidget(self.output_dir)
        
        output_layout.addLayout(output_dir_layout)
        
        self.open_reports = QCheckBox("Open reports after generation")
        output_layout.addWidget(self.open_reports)
        
        layout.addWidget(self.output_group)
        layout.addStretch()
        
        self.update_command()
    
    def toggle_result_selector(self, state):
        """Enable/disable result directory selector based on "all results" checkbox."""
        self.result_dir.setEnabled(not state)
    
    def update_command(self):
        """Update the command preview based on current settings."""
        command = "python scripts/generate_report.py"
        
        if not self.all_results.isChecked():
            result_dir = self.result_dir.get_path()
            if result_dir:
                command += f" --result-dir {result_dir}"
            else:
                self.command_changed.emit("# Please select a result directory or check 'Generate reports for all results'")
                return
        
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the command to execute."""
        command = "python scripts/generate_report.py"
        
        if not self.all_results.isChecked():
            result_dir = self.result_dir.get_path()
            if result_dir:
                command += f" --result-dir {result_dir}"
            else:
                return ""  # Invalid command
        
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        return command


class CombinedReportTab(QWidget):
    """Tab for generating combined/comparison reports."""
    
    command_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Report type
        type_group = QGroupBox("Report Type")
        type_layout = QHBoxLayout(type_group)
        
        self.type_comparison = QRadioButton("Comparison")
        self.type_comparison.setChecked(True)
        self.type_comparison.toggled.connect(self.update_command)
        
        self.type_summary = QRadioButton("Summary")
        self.type_summary.toggled.connect(self.update_command)
        
        type_layout.addWidget(self.type_comparison)
        type_layout.addWidget(self.type_summary)
        
        layout.addWidget(type_group)
        
        # Baseline directory
        baseline_layout = QHBoxLayout()
        baseline_layout.addWidget(QLabel("Baseline Directory:"))
        
        self.baseline_dir = PathSelector(dialog_type="dir", dialog_caption="Select Baseline Directory")
        self.baseline_dir.path_changed.connect(self.update_command)
        baseline_layout.addWidget(self.baseline_dir)
        
        layout.addLayout(baseline_layout)
        
        # Contender directories
        contender_group = QGroupBox("Contender Directories")
        contender_layout = QVBoxLayout(contender_group)
        
        self.contender_list = QListWidget()
        contender_layout.addWidget(self.contender_list)
        
        contender_buttons_layout = QHBoxLayout()
        
        self.add_contender_btn = QPushButton("Add Contender...")
        self.add_contender_btn.clicked.connect(self.add_contender)
        
        self.remove_contender_btn = QPushButton("Remove Selected")
        self.remove_contender_btn.clicked.connect(self.remove_contender)
        
        contender_buttons_layout.addWidget(self.add_contender_btn)
        contender_buttons_layout.addWidget(self.remove_contender_btn)
        
        contender_layout.addLayout(contender_buttons_layout)
        
        layout.addWidget(contender_group)
        
        # Comparison options
        comp_group = QGroupBox("Comparison Options")
        comp_layout = QVBoxLayout(comp_group)
        
        # Compare by options
        compare_by_layout = QHBoxLayout()
        compare_by_layout.addWidget(QLabel("Compare by:"))
        
        self.compare_configs = QRadioButton("Configurations")
        self.compare_configs.setChecked(True)
        self.compare_configs.toggled.connect(self.update_command)
        
        self.compare_flags = QRadioButton("Flags")
        self.compare_flags.toggled.connect(self.update_command)
        
        self.compare_platforms = QRadioButton("Platforms")
        self.compare_platforms.toggled.connect(self.update_command)
        
        compare_by_layout.addWidget(self.compare_configs)
        compare_by_layout.addWidget(self.compare_flags)
        compare_by_layout.addWidget(self.compare_platforms)
        
        comp_layout.addLayout(compare_by_layout)
        
        # Specific configurations
        specific_layout = QHBoxLayout()
        specific_layout.addWidget(QLabel("Specific Items:"))
        
        self.specific_configs = QLineEdit()
        self.specific_configs.setPlaceholderText("e.g., gcc,clang or Debug_O0,Release_O3")
        self.specific_configs.textChanged.connect(self.update_command)
        
        specific_layout.addWidget(self.specific_configs)
        
        comp_layout.addLayout(specific_layout)
        
        layout.addWidget(comp_group)
        
        # Output options
        output_group = QGroupBox("Output Options")
        output_layout = QVBoxLayout(output_group)
        
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(QLabel("Custom Output Directory:"))
        
        self.output_dir = PathSelector(dialog_type="dir", dialog_caption="Select Output Directory")
        self.output_dir.path_changed.connect(self.update_command)
        
        output_dir_layout.addWidget(self.output_dir)
        
        output_layout.addLayout(output_dir_layout)
        
        self.open_reports = QCheckBox("Open reports after generation")
        output_layout.addWidget(self.open_reports)
        
        layout.addWidget(output_group)
        layout.addStretch()
        
        self.update_command()
    
    def add_contender(self):
        """Add a contender directory."""
        path = QFileDialog.getExistingDirectory(
            self, "Select Contender Directory", str(PROJECT_ROOT)
        )
        if path:
            self.contender_list.addItem(path)
            self.update_command()
    
    def remove_contender(self):
        """Remove the selected contender directory."""
        selected_items = self.contender_list.selectedItems()
        for item in selected_items:
            self.contender_list.takeItem(self.contender_list.row(item))
        self.update_command()
    
    def update_command(self):
        """Update the command preview based on current settings."""
        command = "python scripts/generate_combined_report.py"
        
        # Report type
        if self.type_comparison.isChecked():
            command += " --type comparison"
        else:
            command += " --type summary"
        
        # Baseline directory
        baseline_dir = self.baseline_dir.get_path()
        if baseline_dir:
            command += f" --baseline {baseline_dir}"
        else:
            self.command_changed.emit("# Please select a baseline directory")
            return
        
        # Contender directories
        contenders = []
        for i in range(self.contender_list.count()):
            contenders.append(self.contender_list.item(i).text())
        
        if contenders:
            command += f" --contenders {','.join(contenders)}"
        
        # Comparison options
        if self.compare_configs.isChecked():
            command += " --compare-configs"
        elif self.compare_flags.isChecked():
            command += " --compare-flags"
        elif self.compare_platforms.isChecked():
            command += " --compare-platforms"
        
        specific = self.specific_configs.text()
        if specific:
            if self.compare_configs.isChecked():
                command += f" {specific}"
            elif self.compare_flags.isChecked():
                command += f" {specific}"
            elif self.compare_platforms.isChecked():
                command += f" {specific}"
        
        # Output directory
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the command to execute."""
        command = "python scripts/generate_combined_report.py"
        
        # Report type
        if self.type_comparison.isChecked():
            command += " --type comparison"
        else:
            command += " --type summary"
        
        # Baseline directory
        baseline_dir = self.baseline_dir.get_path()
        if baseline_dir:
            command += f" --baseline {baseline_dir}"
        else:
            return ""  # Invalid command
        
        # Contender directories
        contenders = []
        for i in range(self.contender_list.count()):
            contenders.append(self.contender_list.item(i).text())
        
        if contenders:
            command += f" --contenders {','.join(contenders)}"
        
        # Comparison options
        if self.compare_configs.isChecked():
            command += " --compare-configs"
        elif self.compare_flags.isChecked():
            command += " --compare-flags"
        elif self.compare_platforms.isChecked():
            command += " --compare-platforms"
        
        specific = self.specific_configs.text()
        if specific:
            if self.compare_configs.isChecked():
                command += f" {specific}"
            elif self.compare_flags.isChecked():
                command += f" {specific}"
            elif self.compare_platforms.isChecked():
                command += f" {specific}"
        
        # Output directory
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        return command


class PipelineStepWidget(QWidget):
    """Widget representing a pipeline step."""
    
    step_changed = Signal()
    remove_requested = Signal(object)  # Signal to remove this step
    
    def __init__(self, step_type, parent=None):
        super().__init__(parent)
        self.step_type = step_type
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Step type label/icon
        self.type_label = QLabel(step_type.capitalize())
        layout.addWidget(self.type_label)
        
        # Description of what the step will do
        self.description = QLabel("Configure this step")
        layout.addWidget(self.description, 1)  # Stretch
        
        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setMaximumWidth(30)
        self.remove_btn.clicked.connect(lambda: self.remove_requested.emit(self))
        layout.addWidget(self.remove_btn)
    
    def set_description(self, description):
        """Set the step description."""
        self.description.setText(description)
    
    def get_config(self):
        """Get the step configuration."""
        return {}  # Override in subclasses
    
    def set_config(self, config):
        """Set the step configuration."""
        pass  # Override in subclasses


class PipelineTab(QWidget):
    """Tab for defining and executing pipelines."""
    
    command_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Pipeline steps list
        steps_group = QGroupBox("Pipeline Steps")
        steps_layout = QVBoxLayout(steps_group)
        
        self.steps_list = QListWidget()
        self.steps_list.setSelectionMode(QListWidget.SingleSelection)
        steps_layout.addWidget(self.steps_list)
        
        # Step controls
        steps_buttons_layout = QHBoxLayout()
        
        self.add_step_combo = QComboBox()
        self.add_step_combo.addItems(["Create Experiment", "Run Benchmarks", "Generate Report", "Combined Report"])
        steps_buttons_layout.addWidget(self.add_step_combo)
        
        self.add_step_btn = QPushButton("Add Step")
        self.add_step_btn.clicked.connect(self.add_step)
        steps_buttons_layout.addWidget(self.add_step_btn)
        
        self.move_up_btn = QPushButton("Move Up")
        self.move_up_btn.clicked.connect(self.move_step_up)
        steps_buttons_layout.addWidget(self.move_up_btn)
        
        self.move_down_btn = QPushButton("Move Down")
        self.move_down_btn.clicked.connect(self.move_step_down)
        steps_buttons_layout.addWidget(self.move_down_btn)
        
        steps_layout.addLayout(steps_buttons_layout)
        
        layout.addWidget(steps_group)
        
        # Step configuration
        config_group = QGroupBox("Step Configuration")
        self.config_layout = QVBoxLayout(config_group)
        
        # Placeholder for step configuration
        self.config_placeholder = QLabel("Select or add a step to configure it")
        self.config_placeholder.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_placeholder)
        
        layout.addWidget(config_group)
        
        # Save/load pipeline
        save_load_layout = QHBoxLayout()
        
        self.save_pipeline_btn = QPushButton("Save Pipeline...")
        self.save_pipeline_btn.clicked.connect(self.save_pipeline)
        save_load_layout.addWidget(self.save_pipeline_btn)
        
        self.load_pipeline_btn = QPushButton("Load Pipeline...")
        self.load_pipeline_btn.clicked.connect(self.load_pipeline)
        save_load_layout.addWidget(self.load_pipeline_btn)
        
        layout.addLayout(save_load_layout)
        
        self.update_command()
    
    def add_step(self):
        """Add a new step to the pipeline."""
        step_type = self.add_step_combo.currentText()
        step_widget = PipelineStepWidget(step_type)
        step_widget.remove_requested.connect(self.remove_step)
        
        list_item = QListWidgetItem()
        list_item.setSizeHint(step_widget.sizeHint())
        
        self.steps_list.addItem(list_item)
        self.steps_list.setItemWidget(list_item, step_widget)
        
        self.update_command()
    
    def remove_step(self, step_widget):
        """Remove a step from the pipeline."""
        for i in range(self.steps_list.count()):
            if self.steps_list.itemWidget(self.steps_list.item(i)) == step_widget:
                self.steps_list.takeItem(i)
                break
        
        self.update_command()
    
    def move_step_up(self):
        """Move the selected step up in the pipeline."""
        current_row = self.steps_list.currentRow()
        if current_row > 0:
            current_item = self.steps_list.takeItem(current_row)
            self.steps_list.insertItem(current_row - 1, current_item)
            self.steps_list.setCurrentRow(current_row - 1)
            self.update_command()
    
    def move_step_down(self):
        """Move the selected step down in the pipeline."""
        current_row = self.steps_list.currentRow()
        if current_row < self.steps_list.count() - 1:
            current_item = self.steps_list.takeItem(current_row)
            self.steps_list.insertItem(current_row + 1, current_item)
            self.steps_list.setCurrentRow(current_row + 1)
            self.update_command()
    
    def save_pipeline(self):
        """Save the current pipeline to a file."""
        # In a real implementation, this would serialize the pipeline to JSON
        QMessageBox.information(self, "Save Pipeline", "Pipeline saving not yet implemented")
    
    def load_pipeline(self):
        """Load a pipeline from a file."""
        # In a real implementation, this would deserialize a pipeline from JSON
        QMessageBox.information(self, "Load Pipeline", "Pipeline loading not yet implemented")
    
    def update_command(self):
        """Update the command preview based on the current pipeline."""
        if self.steps_list.count() == 0:
            self.command_changed.emit("# Add steps to the pipeline to see the commands")
            return
        
        command = "# Pipeline Commands:\n"
        for i in range(self.steps_list.count()):
            step_widget = self.steps_list.itemWidget(self.steps_list.item(i))
            step_type = step_widget.step_type
            
            # This is a simplified preview - in a real implementation, it would
            # generate proper commands based on step configuration
            if step_type == "Create Experiment":
                command += "# Step 1: Create a new experiment\n"
                command += "python scripts/create_experiment.py ...\n\n"
            elif step_type == "Run Benchmarks":
                command += "# Step 2: Run benchmarks\n"
                command += "python scripts/run_benchmarks.py ...\n\n"
            elif step_type == "Generate Report":
                command += "# Step 3: Generate report\n"
                command += "python scripts/generate_report.py ...\n\n"
            elif step_type == "Combined Report":
                command += "# Step 4: Generate combined report\n"
                command += "python scripts/generate_combined_report.py ...\n\n"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the command to execute the first step in the pipeline."""
        if self.steps_list.count() == 0:
            return ""
        
        # In a real implementation, this would return the command for the first step
        # For now, we just return a placeholder
        return "echo 'Pipeline execution not yet implemented'"


class MainWindow(QMainWindow):
    """Main window for the BenchEverything UI Tool."""
    
    def __init__(self):
        super().__init__()
        
        self.command_thread = None
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowTitle("BenchEverything UI Tool")
        self.setMinimumSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.create_exp_tab = CreateExperimentTab()
        self.run_benchmarks_tab = RunBenchmarksTab()
        self.generate_report_tab = GenerateReportTab()
        self.combined_report_tab = CombinedReportTab()
        self.pipeline_tab = PipelineTab()
        
        # Add tabs to widget
        self.tab_widget.addTab(self.create_exp_tab, "Create Experiment")
        self.tab_widget.addTab(self.run_benchmarks_tab, "Run Benchmarks")
        self.tab_widget.addTab(self.generate_report_tab, "Generate Report")
        self.tab_widget.addTab(self.combined_report_tab, "Combined Report")
        self.tab_widget.addTab(self.pipeline_tab, "Pipeline")
        
        main_layout.addWidget(self.tab_widget)
        
        # Common controls at the bottom
        self.common_controls = CommonControls()
        main_layout.addWidget(self.common_controls)
    
    def setup_connections(self):
        """Set up signal/slot connections."""
        # Connect tab command changes to common controls
        self.create_exp_tab.command_changed.connect(self.common_controls.set_command_preview)
        self.run_benchmarks_tab.command_changed.connect(self.common_controls.set_command_preview)
        self.generate_report_tab.command_changed.connect(self.common_controls.set_command_preview)
        self.combined_report_tab.command_changed.connect(self.common_controls.set_command_preview)
        self.pipeline_tab.command_changed.connect(self.common_controls.set_command_preview)
        
        # Connect tab changes to update command preview
        self.tab_widget.currentChanged.connect(self.update_command_preview)
        
        # Connect common control buttons
        self.common_controls.run_clicked.connect(self.run_command)
        self.common_controls.stop_clicked.connect(self.stop_command)
        self.common_controls.clear_clicked.connect(self.common_controls.clear_output)
    
    def update_command_preview(self):
        """Update command preview when changing tabs."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.create_exp_tab:
            self.create_exp_tab.update_command()
        elif current_tab == self.run_benchmarks_tab:
            self.run_benchmarks_tab.update_command()
        elif current_tab == self.generate_report_tab:
            self.generate_report_tab.update_command()
        elif current_tab == self.combined_report_tab:
            self.combined_report_tab.update_command()
        elif current_tab == self.pipeline_tab:
            self.pipeline_tab.update_command()
    
    def get_current_command(self) -> str:
        """Get the command for the current tab."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.create_exp_tab:
            return self.create_exp_tab.get_command()
        elif current_tab == self.run_benchmarks_tab:
            return self.run_benchmarks_tab.get_command()
        elif current_tab == self.generate_report_tab:
            return self.generate_report_tab.get_command()
        elif current_tab == self.combined_report_tab:
            return self.combined_report_tab.get_command()
        elif current_tab == self.pipeline_tab:
            return self.pipeline_tab.get_command()
        return ""
    
    def run_command(self):
        """Run the current command."""
        command = self.get_current_command()
        if not command:
            QMessageBox.warning(self, "Invalid Command", "Please configure a valid command to run.")
            return
        
        # Update UI state
        self.common_controls.set_running_state(True)
        self.common_controls.append_output(f"Running command: {command}")
        
        # Create and start the command thread
        self.command_thread = CommandThread(command)
        self.command_thread.output_received.connect(
            lambda text: self.common_controls.append_output(text, False)
        )
        self.command_thread.error_received.connect(
            lambda text: self.common_controls.append_output(text, True)
        )
        self.command_thread.command_finished.connect(self.on_command_finished)
        self.command_thread.start()
    
    def stop_command(self):
        """Stop the currently running command."""
        if self.command_thread and self.command_thread.isRunning():
            self.common_controls.append_output("Stopping command...", True)
            self.command_thread.stop()
    
    def on_command_finished(self, exit_code):
        """Handle command completion."""
        if exit_code == 0:
            self.common_controls.append_output("Command completed successfully.")
        else:
            self.common_controls.append_output(f"Command failed with exit code {exit_code}", True)
        
        # Update UI state
        self.common_controls.set_running_state(False)


def main():
    """Main entry point for the BenchEverything UI Tool."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a consistent look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()