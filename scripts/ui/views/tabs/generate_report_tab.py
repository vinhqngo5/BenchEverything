"""Generate report tab for creating reports from benchmark results."""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox
)
from PySide6.QtCore import Signal

from views.widgets.path_selector import PathSelector
from utils.constants import PROJECT_ROOT


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