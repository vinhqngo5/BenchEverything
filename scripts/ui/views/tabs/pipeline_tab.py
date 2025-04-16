"""Tab for defining and executing pipelines."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QComboBox, QListWidget,
    QPushButton, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Signal, Qt

from views.widgets.pipeline_step import PipelineStepWidget


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