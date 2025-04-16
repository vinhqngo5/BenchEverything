"""Tab for generating combined/comparison reports."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QLineEdit,
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
        
        # Experiment selection
        exp_group = QGroupBox("Experiment Selection")
        exp_layout = QVBoxLayout(exp_group)
        
        exp_layout.addWidget(QLabel("Comma-separated list of experiments to include (leave empty for all):"))
        self.experiments = QLineEdit()
        self.experiments.setPlaceholderText("e.g., int_addition,float_addition,container_push_back")
        self.experiments.textChanged.connect(self.update_command)
        
        exp_layout.addWidget(self.experiments)
        
        layout.addWidget(exp_group)
        
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
        else:
            self.command_changed.emit("# Please add at least one contender directory")
            return
        
        # Experiments
        experiments = self.experiments.text().strip()
        if experiments:
            command += f" --experiments {experiments}"
        
        # Output directory
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        self.command_changed.emit(command)
    
    def get_command(self) -> str:
        """Get the command to execute."""
        command = "python scripts/generate_combined_report.py"
        
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
        else:
            return ""  # Invalid command
        
        # Experiments
        experiments = self.experiments.text().strip()
        if experiments:
            command += f" --experiments {experiments}"
        
        # Output directory
        output_dir = self.output_dir.get_path()
        if output_dir:
            command += f" --output-dir {output_dir}"
        
        return command