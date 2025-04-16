"""Custom widget for selecting file/directory paths."""

import os
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton,
    QFileDialog
)
from PySide6.QtCore import Signal

from utils.constants import PROJECT_ROOT


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