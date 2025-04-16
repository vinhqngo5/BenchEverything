"""Tab for creating new benchmark experiments."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QGroupBox, QCheckBox
)
from PySide6.QtCore import Signal
from utils import create_experiment


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
        
        # Instead of a complex embedded Python command, we now use a simple
        # Python command that calls our utility function
        cmd = f"""python -c "
from scripts.ui.utils import create_experiment

# Call the create_experiment function with parameters from the UI
messages = create_experiment(
    '{exp_name}',
    create_benchmark_cpp={self.create_benchmark_cpp.isChecked()},
    update_cmake={self.update_cmake.isChecked()},
    update_config={self.update_config.isChecked()}
)

# Print all messages from the function
for message in messages:
    print(message)
"
"""
        return cmd
    
    def clear_fields(self):
        """Clear all input fields."""
        self.exp_name_input.clear()
        self.create_benchmark_cpp.setChecked(True)
        self.update_cmake.setChecked(True)
        self.update_config.setChecked(True)