"""Widget representing a pipeline step."""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Signal


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