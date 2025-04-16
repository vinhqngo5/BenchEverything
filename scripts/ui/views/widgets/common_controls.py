"""Common controls shared across all tabs."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QGroupBox
)
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Signal


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