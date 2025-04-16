"""Tab for generating combined/comparison reports."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QRadioButton, QLineEdit,
    QListWidget, QPushButton, QFileDialog
)
from PySide6.QtCore import Signal

from utils.constants import PROJECT_ROOT
from views.widgets.path_selector import PathSelector


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