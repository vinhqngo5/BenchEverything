#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Import the MainWindow class from the views module
from views.main_window import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    """Main entry point for the BenchEverything UI Tool."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a consistent look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()