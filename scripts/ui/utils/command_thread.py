"""Thread for executing commands without blocking the UI."""

import subprocess
import threading
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
    
    def _read_output(self, stream, is_error):
        """Read from the stream and emit signals."""
        for line in iter(stream.readline, ''):
            if self.stopped:
                break
            if is_error:
                self.error_received.emit(line.rstrip())
            else:
                self.output_received.emit(line.rstrip())
    
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
            
            # Create threads to read stdout and stderr concurrently
            stdout_thread = threading.Thread(
                target=self._read_output, 
                args=(self.process.stdout, False)
            )
            stderr_thread = threading.Thread(
                target=self._read_output, 
                args=(self.process.stderr, True)
            )
            
            # Start the threads
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
            
            # Wait for process to complete
            exit_code = self.process.wait()
            
            # Wait for output threads to finish
            stdout_thread.join()
            stderr_thread.join()
            
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