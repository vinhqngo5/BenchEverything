"""Thread for executing commands without blocking the UI."""

import subprocess
from PySide6.QtCore import QThread, Signal


class CommandThread(QThread):
    """Thread for executing commands without blocking the UI."""
    output_received = Signal(str)
    error_received = Signal(str)
    command_finished = Signal(int)
    
    def __init__(self, command: str):
        super().__init__()
        self.command = command
        self.process = None
        self.stopped = False
    
    def run(self):
        """Execute the command and process its output."""
        try:
            # Start the process
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                shell=True
            )
            
            # Read stdout
            for line in iter(self.process.stdout.readline, ''):
                if self.stopped:
                    break
                self.output_received.emit(line.rstrip())
            
            # Read stderr
            for line in iter(self.process.stderr.readline, ''):
                if self.stopped:
                    break
                self.error_received.emit(line.rstrip())
            
            # Wait for process to complete
            exit_code = self.process.wait()
            if not self.stopped:
                self.command_finished.emit(exit_code)
        
        except Exception as e:
            self.error_received.emit(f"Error running command: {str(e)}")
            self.command_finished.emit(1)
    
    def stop(self):
        """Stop the running command."""
        if self.process and self.process.poll() is None:
            self.stopped = True
            self.process.terminate()
            self.process.wait(timeout=3)
            # Force kill if not terminated after timeout
            if self.process.poll() is None:
                self.process.kill()