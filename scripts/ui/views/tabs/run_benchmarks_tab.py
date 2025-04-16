"""Tab for running benchmark experiments."""

import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QPushButton, QComboBox, QCheckBox,
    QLineEdit, QGroupBox, QFormLayout
)
from PySide6.QtCore import Signal

from utils.constants import PROJECT_ROOT
from views.widgets.path_selector import PathSelector


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
        default_config_path = str(PROJECT_ROOT / "config" / "benchmark_config.json")
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
            config_path = PROJECT_ROOT / "config" / "benchmark_config.json"
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