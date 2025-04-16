# BenchEverything UI Tool Design Document

## Overview

The BenchEverything UI Tool is a Python-based graphical interface that streamlines common workflows when working with the BenchEverything benchmark framework. It integrates the existing command-line scripts (`run_benchmarks.py`, `generate_report.py`, and `generate_combined_report.py`) into a single, unified interface.

## Design Goals

1. **Simplify Workflows**: Make it easier to execute typical benchmark tasks
2. **Unified Interface**: Combine multiple command-line tools into one GUI
3. **Pipeline Support**: Allow definition and execution of multi-step workflows
4. **Live Feedback**: Show command outputs in real-time
5. **Extensibility**: Support future additions to the BenchEverything framework
6. **User-Friendly**: Provide an intuitive interface for users with varying levels of expertise

## Framework Choice

**PySide6** (Qt for Python) has been selected as the GUI framework because:
- Cross-platform compatibility (Windows, macOS, Linux)
- Rich set of widgets and controls
- Good support for threading (essential for non-blocking UI while running commands)
- Modern look and feel
- Strong community support
- Permissive LGPL license (compared to PyQt's GPL)

## UI Architecture

### Overall Structure

The UI is organized around a tabbed interface with common controls:

```
┌─────────────────────────────────────────────────────────────────────┐
│ BenchEverything UI Tool                                  [_] [□] [X] │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │
│ │  Create  │ │   Run   │ │ Reports │ │Combined │ │    Pipeline     │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ [Tab-specific controls and inputs]                                   │
│                                                                     │
│                                                                     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ Command to be executed:                                             │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ python scripts/run_benchmarks.py --experiments int_addition ...  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ Output:                                                              │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │                                                                 │ │
│ │ [Console output appears here]                                   │ │
│ │                                                                 │ │
│ │                                                                 │ │
│ │                                                                 │ │
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ [Clear Output]                          [Stop]         [Run Command] │
└─────────────────────────────────────────────────────────────────────┘
```

### Tab Details

#### 1. Create Experiment Tab

**Purpose**: Create new benchmark experiment directories with correct structure and files.

**Controls**:
- Experiment Name: Text input
- Template Options: Checkboxes for:
  - Create basic `benchmark.cpp`
  - Auto-update main `CMakeLists.txt` (with warning about file modification)
  - Auto-update `benchmark_config.json` (with warning)

**Actions**:
- The "Run Command" button triggers experiment creation
- Command preview shows the equivalent manual commands that would be run

#### 2. Run Benchmarks Tab

**Purpose**: Configure and execute benchmark runs.

**Controls**:
- Path to config: Path selector (default: benchmark_config.json). When path to config is reloaded, auto reload the Experiment and Compiler selection.
- Experiment Selection: Checklist populated from config with "Select All/None" buttons
- Compiler Selection: Checklist with "Select All/None" buttons
- Build Flags: Dropdown with common options + text input for custom flags
- Options:
  - Force re-run: Checkbox
  - Incremental build: Checkbox
- Additional Options (collapsible):
  - Extra flags for `run_benchmarks.py`

**Actions**:
- The "Run Command" button executes the benchmark with selected options
- Command preview shows the equivalent `run_benchmarks.py` command

#### 3. Generate Reports Tab

**Purpose**: Generate reports from benchmark results.

**Controls**:
- Result Directory: Path selector with browse button
  - Option to select "Generate reports for all results"
- Output Options: 
  - Custom output directory: Path selector
  - Open reports after generation: Checkbox

**Actions**:
- The "Run Command" button triggers report generation
- Command preview shows the equivalent `generate_report.py` command

#### 4. Combined Reports Tab

**Purpose**: Generate comparison reports between different configurations.

**Controls**:
- Report Type: Radio buttons (Comparison, Summary)
- Baseline Directory: Path selector
- Contender Directories: List widget with Add/Remove buttons
- Comparison Options:
  - Compare by: Radio buttons (Configurations, Flags, Platforms)
  - Specific configurations: Text input
- Output Options:
  - Custom output directory: Path selector
  - Open reports after generation: Checkbox

**Actions**:
- The "Run Command" button triggers combined report generation
- Command preview shows the equivalent `generate_combined_report.py` command

#### 5. Pipeline Tab

**Purpose**: Define, save, and run sequences of benchmark operations.

**Controls**:
- Pipeline Steps: List widget showing defined steps with Up/Down/Remove buttons
- Add Step: Dropdown to select step type + "Add" button
- Step Configuration: Panel that shows configuration for the currently selected step
- Save/Load Pipeline: Buttons to save current pipeline or load a saved one

**Actions**:
- The "Run Command" button executes all steps in the pipeline in sequence
- Command preview shows the command for the current/next step

### Common Elements

**Command Preview**:
- A read-only text area showing the command that will be executed
- Updates dynamically as options are changed
- Helps users learn the command-line interface

**Output Console**:
- A text area for showing real-time output from executed commands
- Scrollable with automatic scrolling to the bottom as new output appears
- Context menu with copy/select all options

**Control Buttons**:
- Clear Output: Clears the output console
- Stop: Terminates the currently running command (disabled when no command is running)
- Run Command: Executes the current command (disabled while a command is running)

## Technical Implementation

### Process Execution

Commands will be executed in a separate process using Python's `subprocess` module:

```python
process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,  # Line buffered
    shell=True
)
```

### Threading

To prevent UI freezing, command execution and output reading will be handled in a separate thread:

```python
class CommandThread(QThread):
    output_received = Signal(str)
    command_finished = Signal(int)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None
        
    def run(self):
        # Start process
        self.process = subprocess.Popen(...)
        
        # Read output asynchronously
        while True:
            line = self.process.stdout.readline()
            if not line and self.process.poll() is not None:
                break
            self.output_received.emit(line)
            
        # Signal completion
        exit_code = self.process.wait()
        self.command_finished.emit(exit_code)
    
    def stop(self):
        if self.process:
            self.process.terminate()
```

### Pipeline Implementation

Pipelines will be represented as a sequence of steps, each with its own configuration:

```python
class PipelineStep:
    def __init__(self, step_type, config=None):
        self.step_type = step_type  # 'create', 'run', 'report', or 'combined'
        self.config = config or {}  # Step-specific configuration
        
    def get_command(self):
        # Generate command based on step_type and config
        
    def to_dict(self):
        # Serialize step for saving
        
    @classmethod
    def from_dict(cls, data):
        # Deserialize step from saved data
```

Pipelines will be saved as JSON files in a `pipelines/` directory.

### Path Selection

Path selection will be implemented with a composite widget containing:
- Text input field for manual path entry
- "Browse" button that opens an appropriate file/directory dialog
- Optional "Show in Explorer/Finder" button

## Data Flow

1. **UI Initialization**:
   - Read `benchmark_config.json` to populate experiment and compiler lists
   - Set up signal/slot connections for UI interactions

2. **Command Execution**:
   - User configures options in UI
   - Command string is generated and displayed in preview area
   - User clicks "Run Command"
   - UI creates and starts command thread
   - Thread executes command, emitting output
   - UI displays output in real-time
   - On completion, UI updates state (re-enable buttons, etc.)

3. **Pipeline Execution**:
   - Similar to command execution, but steps run sequentially
   - Each step waits for the previous step to complete
   - Output is annotated to indicate which step is running
   - If a step fails, pipeline either stops or continues based on configuration

## Error Handling

1. **Process Errors**:
   - Standard error output is captured and displayed in the output console
   - Non-zero exit codes are reported with a status message
   - The UI remains responsive even if commands fail

2. **UI Validation**:
   - Basic validation for required fields
   - Warning dialogs for potentially destructive actions
   - Help text to guide users in correct input

3. **Recovery**:
   - Option to retry failed commands
   - Clear indication of what might have gone wrong

## Future Extensions

The UI is designed to accommodate future enhancements:

1. **Result/Report Browser**:
   - Add a file browser panel for exploring results and reports
   - Double-click to open reports in the default application
   - Context menu with common actions

2. **Configuration Editor**:
   - Provide a UI for editing `benchmark_config.json`
   - Add/remove experiments and compilers

3. **Template Management**:
   - UI for managing and creating experiment templates

4. **Performance Visualization**:
   - Integrate with report visuals to display graphs directly in the UI

## Implementation Plan

### Phase 1: Core Framework

1. Set up basic UI structure with tabs
2. Implement command execution and output display
3. Implement path selection widgets

### Phase 2: Individual Tabs

1. Implement Run Benchmarks tab
2. Implement Report Generation tab
3. Implement Combined Report tab
4. Implement Create Experiment tab

### Phase 3: Pipeline Support

1. Implement pipeline data structures
2. Create pipeline UI
3. Add save/load functionality
4. Implement pipeline execution

### Phase 4: Polish and Extensions

1. Add error handling and validation
2. Improve UI styling and usability
3. Add help text and tooltips
4. Implement selected extensions