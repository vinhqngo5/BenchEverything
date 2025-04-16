"""Main window for the BenchEverything UI Tool."""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QMessageBox, QStatusBar
)
from PySide6.QtCore import Qt

from utils.command_thread import CommandThread
from views.widgets.common_controls import CommonControls
from views.tabs.create_experiment_tab import CreateExperimentTab
from views.tabs.run_benchmarks_tab import RunBenchmarksTab
from views.tabs.generate_report_tab import GenerateReportTab
from views.tabs.combined_report_tab import CombinedReportTab
from views.tabs.pipeline_tab import PipelineTab


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
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop any running command
        if self.command_thread and self.command_thread.isRunning():
            self.command_thread.stop()
            self.command_thread.wait()
        
        event.accept()