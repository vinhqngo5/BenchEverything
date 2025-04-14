# BenchEverything Project Documentation

## Table of Contents

*   [1. Introduction](#1-introduction)
    *   [1.1. Goal](#11-goal)
    *   [1.2. Core Philosophy](#12-core-philosophy)
*   [2. Core Concepts](#2-core-concepts)
*   [3. Directory Structure](#3-directory-structure)
*   [4. Workflow](#4-workflow)
    *   [4.1. Add Experiment](#41-add-experiment)
    *   [4.2. Configure Run](#42-configure-run)
    *   [4.3. Run Benchmarks (`run_benchmarks.py`)](#43-run-benchmarks-run_benchmarkspy)
    *   [4.4. Generate Single Report (`generate_report.py`)](#44-generate-single-report-generate_reportpy)
    *   [4.5. Generate Combined Reports (`generate_combined_report.py`)](#45-generate-combined-reports-generate_combined_reportpy)
    *   [4.6. Cross-Machine/Compiler Workflow](#46-cross-machinecompiler-workflow)
*   [5. Configuration (`run_benchmarks.py`)](#5-configuration-run_benchmarkspy)
    *   [5.1. Responsibilities](#51-responsibilities)
    *   [5.2. Toolchain Files](#52-toolchain-files)
    *   [5.3. Build Management](#53-build-management)
    *   [5.4. Overrides (`exp_config.json`)](#54-overrides-exp_configjson)
*   [6. Data Collection Details](#6-data-collection-details)
    *   [6.1. Google Benchmark](#61-google-benchmark)
    *   [6.2. Perf (Linux)](#62-perf-linux)
    *   [6.3. Assembly](#63-assembly)
    *   [6.4. Metadata (`metadata.json`)](#64-metadata-metadatajson)
    *   [6.5. Data Commits](#65-data-commits)
*   [7. Reporting](#7-reporting)
    *   [7.1. Single Report Generation (`generate_report.py`)](#71-single-report-generation-generate_reportpy)
        *   [7.1.1. Report Structure & Assets](#711-report-structure--assets)
        *   [7.1.2. `pre_report.py` Integration](#712-pre_reportpy-integration)
        *   [7.1.3. Template Placeholders](#713-template-placeholders)
        *   [7.1.4. Handling Failures](#714-handling-failures)
    *   [7.2. Combined Report Generation (`generate_combined_report.py`)](#72-combined-report-generation-generate_combined_reportpy)
        *   [7.2.1. Report Types (Summary, Comparison)](#721-report-types-summary-comparison)
        *   [7.2.2. Comparison Assets](#722-comparison-assets)
        *   [7.2.3. Templates for Combined Reports](#723-templates-for-combined-reports)
    *   [7.3. Godbolt Integration](#73-godbolt-integration)
*   [8. Extensibility Guide](#8-extensibility-guide)
    *   [8.1. Adding a New Profiler](#81-adding-a-new-profiler)
    *   [8.2. Adding Custom Analysis/Plots](#82-adding-custom-analysisplots)
    *   [8.3. Supporting New Platforms](#83-supporting-new-platforms)
*   [9. Usage](#9-usage)
    *   [9.1. Prerequisites](#91-prerequisites)
    *   [9.2. Basic Steps](#92-basic-steps)
    *   [9.3. Benchmarking Tips](#93-benchmarking-tips)
*   [10. Future Considerations](#10-future-considerations)

---

## 1. Introduction

### 1.1. Goal

To provide a structured C++ benchmarking repository using Google Benchmark and CMake. It facilitates running experiments across various configurations (platforms, compilers, flags), collecting detailed performance data (benchmark timings, perf counters, assembly), and generating comparative reports.

### 1.2. Core Philosophy

*   **Experiment-centric:** Each benchmark lives in its own isolated directory under `experiments/`.
*   **Reproducibility:** Results are tagged with configuration details (platform, compiler, flags) and a unique metadata hash. Builds are clean by default.
*   **Centralized Configuration:** A primary Python script (`scripts/run_benchmarks.py`), potentially driven by config files, acts as the main user interface for defining *what* to run and *how*.
*   **Extensibility:** The structure and scripts are designed to be easily modified to add new tools, metrics, platforms, or reporting formats.

---

## 2. Core Concepts

*   **Experiment:** A specific piece of code being benchmarked, located under `experiments/<experiment_name>/`. Contains C++ source(s), its own `CMakeLists.txt`, a report template (`README.md.template`), and optional configuration overrides (`exp_config.json`) and pre-report analysis scripts (`pre_report.py`).
*   **Configuration:** A unique combination defining the build and runtime environment. Key elements:
    *   Platform Identifier (e.g., `linux-x86_64`, `macos-arm64`)
    *   Compiler Identifier (e.g., `gcc-11.2.0`, `clang-14.0.1`, `msvc-19.32`)
    *   Build Flags Identifier (e.g., `Release_O3_native`, `Debug_O0_avx2`). This combines CMake Build Type (`Release`, `Debug`, `RelWithDebInfo`) with key optimization/architecture flags.
    *   Metadata Hash: A hash generated from the combination of platform, compiler, build flags, and timestamp, used to uniquely identify experiment runs.
*   **Result:** Raw output data collected from running one experiment under a specific configuration. Stored under `results/` following a path derived from the Configuration. See [Section 3](#3-directory-structure).
*   **Report:** Human-readable Markdown files generated from one or more results. Stored under `reports/`, mirroring the `results/` structure and including generated assets like plots. See [Section 7.1](#711-report-structure--assets).

---

## 3. Directory Structure

````text
BenchEverything/
├── .git/
├── .gitignore
├── README.md # Top-level project info, setup
├── CMakeLists.txt # Root CMakeLists, finds common dependencies (like GBench), includes experiments/
├── cmake/ # CMake helper modules
│   ├── BenchmarkUtils.cmake # Helper add_benchmark_experiment function
│   ├── Dependencies.cmake # (Optional) Centralized FetchContent_Declare for common libs
│   └── toolchains/ # Directory for CMake toolchain files (e.g., gcc11.cmake, clang14.cmake)
├── scripts/ # Python helper scripts
│   ├── run_benchmarks.py # *** Central script to configure and run benchmarks ***
│   ├── generate_report.py # Script to generate a single markdown report from one result
│   ├── generate_combined_report.py # Script to generate summary/comparison reports
│   ├── config/ # Configuration files (e.g., YAML/JSON) for run_benchmarks.py
│   └── requirements.txt # Python dependencies (PyYAML, matplotlib, pandas, etc.)
├── third_party/ # Dependencies managed via FetchContent or submodules (GBench often here)
├── experiments/ # === Individual Benchmarks ===
│   └── <experiment_name>/
│       ├── CMakeLists.txt # Defines target, finds/links deps (uses find_package/FetchContent)
│       ├── src/ # C++ source files for the benchmark
│       │   └── benchmark.cpp
│       ├── README.md.template # Report template with placeholders (see Section 7.3)
│       ├── exp_config.json # (Optional) Overrides for global settings (flags, perf events)
│       └── pre_report.py # (Optional) Python script to generate plots/figures from results
├── build/ # === Build Artifacts === (Generally gitignored)
│   └── <platform>/
│       └── <compiler_id>/
│           └── <build_flags_id>/ # CMake build directory for one configuration
│               └── ... (CMake cache, object files, executables)
├── results/ # === Raw Output Data === (Committing this is planned, monitor size)
│   └── <platform>/ # e.g., linux-x86_64
│       └── <compiler_id>/ # e.g., gcc-11.2.0
│           └── <build_flags_id>/ # e.g., Release_O3_native
│               └── <metadata_hash>/ # e.g., a1b2c3d4 (hash based on platform, compiler, build flags, timestamp)
│                   ├── <experiment_name>/
│                   │   ├── benchmark_output.json # Google Benchmark raw JSON
│                   │   ├── perf_stat.log # perf stat text output
│                   │   ├── assembly/ # Directory for assembly snippets
│                   │   │   └── <BM_Function_Name>.s
│                   │   └── metadata.json # Timestamp, metadata hash, metadata source, flags, perf cmd, env...
│                   └── ... (other experiments for this config & hash)
└── reports/ # === Generated Reports === (Intended to be committed)
    └── <platform>/
        └── <compiler_id>/
            └── <build_flags_id>/
                └── <metadata_hash>/
                    ├── <experiment_name>/ # Directory for this specific report instance
                    │   ├── report.md # The final Markdown report (from generate_report.py)
                    │   └── assets/ # Subdir for assets specific to this report
                    │       └── timing_plot.png # Figures generated by pre_report.py
                    │       └── perf_data.csv # Other artifacts
                    ├── <experiment_name_2>/
                    │   ├── report.md
                    │   └── assets/
                    │       └── ...
                    ├── ALL_EXPERIMENTS_SUMMARY.md # Optional: Summary (from generate_combined_report.py)
                    └── comparisons/ # Reports comparing across configs/hashes (from generate_combined_report.py)
                        ├── <comparison_name>.md # e.g., ExpA_GCC_vs_Clang_a1b2c3d4.md
                        └── assets/ # Assets generated specifically for comparisons
                            └── <comparison_name>/
                                └── gcc_vs_clang_timing.png
````

---

## 4. Workflow

The typical process for adding and running benchmarks:

### 4.1. Add Experiment

1.  Create the directory `experiments/<experiment_name>/`.
2.  Write C++ benchmark code in `experiments/<experiment_name>/src/`, using Google Benchmark macros (e.g., `BENCHMARK`, `BENCHMARK_F`). Use fixtures for shared setup/teardown.
3.  Create `experiments/<experiment_name>/CMakeLists.txt`. Use helper functions (like `add_benchmark_experiment` from `cmake/BenchmarkUtils.cmake`) to define the executable target. Use `find_package` or `FetchContent_MakeAvailable` to declare and link experiment-specific dependencies (common dependencies like GBench should be handled by the root `CMakeLists.txt` or `cmake/Dependencies.cmake`).
4.  Create the report template `experiments/<experiment_name>/README.md.template` with explanatory text and [Placeholders](#713-template-placeholders).
5.  *(Optional)* Create `experiments/<experiment_name>/exp_config.json` to override global run configurations (e.g., add specific compiler flags, change perf events) for this experiment only. See [Section 5.4](#54-overrides-exp_configjson).
6.  *(Optional)* Create `experiments/<experiment_name>/pre_report.py` if you need custom plots or data processing during report generation. See [Section 7.1.2](#712-pre_reportpy-integration).
7.  Ensure the experiment is discoverable (e.g., the root `CMakeLists.txt` uses `add_subdirectory` to include `experiments/<experiment_name>`).

### 4.2. Configure Run

Modify `scripts/run_benchmarks.py` or its associated configuration file (e.g., `scripts/config/my_run.yaml`) to define:
*   **Target Configurations:** A list or matrix of compilers, build flag sets (e.g., `Release_O3_native`), platforms.
*   **Target Experiments:** Which experiments to run (`--all`, `--experiments <name1>,<name2>`, `--experiments-matching <pattern>`).
*   **Global Settings:** Default Google Benchmark arguments (`--benchmark_repetitions`), default `perf` events.
*   **Behavior Flags:** Whether to force re-runs (`--force`), use incremental builds (`--incremental-build`).

### 4.3. Run Benchmarks (`run_benchmarks.py`)

Execute the main script: `python scripts/run_benchmarks.py [options]`

The script performs the following for each selected (experiment, configuration) pair:

1.  **Identify Context:** Determines the current Git hash and combines it with the configuration to define the target `build/`, `results/`, and `reports/` paths.
2.  **Check Existence:** Looks for the target `results/.../<git_hash>/<exp_name>` directory. If it exists and `--force` is **not** used, it prompts the user to skip or overwrite. If `--force` is used, it proceeds.
3.  **Merge Config:** Loads the global configuration, checks for `experiments/<exp_name>/exp_config.json`, and merges/overrides settings (flags, perf events) to get the final configuration for this run.
4.  **Prepare Build:**
    *   Selects the appropriate CMake [Toolchain File](#52-toolchain-files) based on the configuration.
    *   Unless `--incremental-build` is specified, it cleans the corresponding `build/...` directory.
    *   Invokes CMake: `cmake -S . -B <build_dir> -DCMAKE_TOOLCHAIN_FILE=<path> -DCMAKE_BUILD_TYPE=<Type> -DCUSTOM_CXX_FLAGS="<flags>" ...`
5.  **Build:** Compiles *only* the target experiment: `cmake --build <build_dir> --target <exp_name>_benchmark`. It logs build errors and continues to the next experiment/configuration if a build fails.
6.  **List Tests:** Runs the compiled benchmark with `--benchmark_list_tests=true` (or parses initial JSON) to get the exact names of registered benchmark functions (crucial for [Assembly Extraction](#63-assembly)).
7.  **Run & Profile:**
    *   Executes the benchmark, saving Google Benchmark JSON output: `<executable> --benchmark_format=json --benchmark_out=<results/.../benchmark_output.json> [gbench_args]`.
    *   If on Linux, wraps the execution with `perf stat`: `perf stat -o <results/.../perf_stat.log> -e <event_list> <executable> ...`. Logs errors if `perf` fails (e.g., invalid event) but continues execution.
    *   Extracts assembly code for listed benchmark functions using `objdump`. See [Section 6.3](#63-assembly).
    *   Saves all outputs and detailed `metadata.json` ([Section 6.4](#64-metadata-metadatajson)) to the `results/.../<git_hash>/<exp_name>/` directory.
8.  Logs runtime errors/crashes and continues execution.

### 4.4. Generate Single Report (`generate_report.py`)

Execute the single report generation script: `python scripts/generate_report.py [options]`

This script focuses on generating a report for **one specific experiment result**.

Options control which result to process (e.g., `--result-dir <path_to_result>`).

1.  **Identify Result:** Takes the path to a specific `results/.../<exp_name>` directory as input.
2.  **Determine Paths:** Calculate the corresponding report path `reports/.../<exp_name>/` and asset path `.../assets/`. Create directories if needed.
3.  **Run Pre-Report Script:** If `experiments/<exp_name>/pre_report.py` exists, execute it, passing the results directory and the target `assets/` directory. See [Section 7.1.2](#712-pre_reportpy-integration).
4.  **Parse Data:** Read `benchmark_output.json`, `perf_stat.log`, `metadata.json`.
5.  **Scan Assets:** List files in the `assets/` directory generated by `pre_report.py`.
6.  **Populate Template:** Process `experiments/<exp_name>/README.md.template`, replacing [Placeholders](#713-template-placeholders) with parsed data, formatted tables, links to assembly, and Markdown for discovered/referenced assets. See [Section 7.1.4](#714-handling-failures) for error handling.
7.  Write the final report to `reports/.../<exp_name>/report.md`.

### 4.5. Generate Combined Reports (`generate_combined_report.py`)

Execute the combined report generation script: `python scripts/generate_combined_report.py [options]`

This script generates reports that aggregate data from **multiple** experiment results, such as summaries or comparisons.

Options control which results to aggregate (`--results-base-dir`, `--hashes`, `--configs`, `--experiments`) and the type of report (`--type summary|comparison`).

1.  **Scan Results:** Finds relevant `results/.../<exp_name>` directories based on filters provided (e.g., across multiple hashes, configs, or experiments).
2.  **Aggregate Data:** Reads data (`metadata.json`, `benchmark_output.json`, etc.) from all selected result directories.
3.  **Perform Analysis (if Comparison):** For comparison reports, calculate differences, ratios, etc., between the selected result sets.
4.  **Generate Combined Assets:** May generate new plots or data files summarizing or comparing the aggregated data. These are typically saved to specific locations like `reports/comparisons/assets/` or within the summary report's directory.
5.  **Populate Template:** Uses a dedicated template (e.g., `scripts/templates/summary_report.md.template`, `scripts/templates/comparison_report.md.template`) and populates it with the aggregated/compared data and links to generated assets.
6.  **Write Report:** Saves the final summary or comparison report (e.g., `reports/.../<git_hash>/ALL_EXPERIMENTS_SUMMARY.md`, `reports/comparisons/<comparison_name>.md`).

### 4.6. Cross-Machine/Compiler Workflow

1.  Develop/modify experiments, commit changes, push to Git remote.
2.  On Machine A (e.g., Linux/GCC): `git pull`, configure `run_benchmarks.py` for GCC targets, run it. Run `generate_report.py` for individual results if desired. Commit/push results & reports.
3.  On Machine B (e.g., Linux/Clang or Windows/MSVC): `git pull`, configure `run_benchmarks.py` for Clang/MSVC targets, run it. Run `generate_report.py` for individual results if desired. Commit/push results & reports.
4.  Locally (or anywhere with access to all results): `git pull`.
    *   Run `generate_report.py --result-dir <path>` to view/regenerate any specific single report.
    *   Run `generate_combined_report.py` with appropriate filters (`--compare-configs`, `--compare-hashes`) to create summary or comparison reports spanning the collected data. Commit/push combined reports.

---

## 5. Configuration (`run_benchmarks.py`)

The `scripts/run_benchmarks.py` script (potentially loading config from YAML/JSON in `scripts/config/`) is the central point for controlling benchmark execution.

### 5.1. Responsibilities

*   Parsing command-line arguments (`--experiments`, `--configs`, `--force`, `--incremental-build`, etc.).
*   Defining the matrix of configurations (compilers, build flags, platforms) to run.
*   Selecting experiments based on user input.
*   Merging global settings with per-experiment overrides ([Section 5.4](#54-overrides-exp_configjson)).
*   Selecting and applying the correct CMake [Toolchain File](#52-toolchain-files).
*   Managing the [Build Process](#53-build-management) (clean vs. incremental).
*   Invoking CMake, the build tool, the benchmark executable, and profiling tools (`perf`).
*   Orchestrating the collection and storage of results.

### 5.2. Toolchain Files

Using CMake toolchain files (e.g., `cmake/toolchains/gcc11.cmake`) is the recommended approach for specifying compilers and related settings. `run_benchmarks.py` should select the appropriate file based on the target configuration and pass it to CMake via `-DCMAKE_TOOLCHAIN_FILE=...`. This provides a robust way to manage different compiler versions and cross-compilation setups.

Example `gcc11.cmake`:
```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_C_COMPILER /usr/bin/gcc-11)
set(CMAKE_CXX_COMPILER /usr/bin/g++-11)
# Add other flags, sysroot settings if needed
```

### 5.3. Build Management

*   **Default:** Clean builds. Before running CMake for a configuration, `run_benchmarks.py` should remove the corresponding `build/<platform>/<compiler>/<flags>/` directory to ensure no artifacts from previous runs interfere.
*   **Option:** `--incremental-build` flag can be provided to skip the cleaning step, allowing CMake to reuse existing artifacts for faster iteration during development. Use with caution, as it may hide configuration issues.
*   Build Directory: `build/` follows the same hierarchy as `results/` and `reports/`.

### 5.4. Overrides (`exp_config.json`)

An optional `experiments/<experiment_name>/exp_config.json` file allows customizing the run for a specific experiment. `run_benchmarks.py` merges this with the global configuration before invoking tools.

Example `exp_config.json`:
```json
{
  "cmake_flags": "-DSPECIAL_FEATURE=ON",
  "cxx_flags": "-Wextra -Werror",
  "perf_events": ["cycles", "instructions", "cache-references", "cache-misses"],
  "gbench_args": "--benchmark_min_time=1.0"
}
```

---

## 6. Data Collection Details

The `run_benchmarks.py` script orchestrates the collection of various data points into the `results/.../<git_hash>/<exp_name>/` directory.

### 6.1. Google Benchmark

*   Executed with `--benchmark_format=json --benchmark_out=<path>/benchmark_output.json`.
*   Additional arguments (e.g., `--benchmark_repetitions`) can be passed via global config or `exp_config.json`.
*   The JSON output contains detailed timing information (mean, median, stddev), iterations, time unit, etc., for each benchmark run.

### 6.2. Perf (Linux)

*   Benchmark execution is wrapped: `perf stat -o <path>/perf_stat.log -e <event_list> <executable> [args]`.
*   The `<event_list>` is configurable globally or via `exp_config.json`. Defaults might include `cycles,instructions,branch-instructions,branch-misses`.
*   If `perf stat` fails (e.g., invalid event name, insufficient permissions), the error is logged to the console, but `run_benchmarks.py` continues. The `perf_stat.log` might be missing or contain error messages. This failure is noted during [Report Generation](#714-handling-failures).
*   Raw `perf record` data (`perf.data`) is **not** typically saved due to size, unless specifically configured for deep-dive analysis.

### 6.3. Assembly

1.  **Identify Functions:** After build, run `<executable> --benchmark_list_tests=true` or parse the `benchmark_output.json` to get the exact list of registered benchmark names (e.g., `BM_MyFunction/16`, `MyFixture_Test/BM_Variant/process_time`).
2.  **Disassemble:** Run `objdump -d --no-show-raw-insn -C <executable_path> | c++filt > full_disassembly.txt` (optional, for debugging).
3.  **Extract Snippets:** Use scripting (Python within `run_benchmarks.py`) to parse the `objdump` output. For each identified benchmark function name, find its corresponding label (e.g., `_Z12BM_MyFunction...:` or the demangled name) and extract the assembly lines until the next function label or `.size` directive. Save each snippet to `assembly/<BM_Function_Name>.s`. Handle potential name mangling differences.

### 6.4. Metadata (`metadata.json`)

A crucial file capturing the execution context:
```json
{
  "timestamp_iso": "2023-10-27T10:30:00Z",
  "git_commit_short": "abc1234",
  "git_commit_full": "abc1234def5678...",
  "platform_id": "linux-x86_64",
  "compiler_id": "gcc-11.2.0",
  "build_flags_id": "Release_O3_native",
  "environment": {
    "uname": "Linux hostname 5.15.0-...",
    "cpu_info": "Intel(R) Core(TM) i7-...",
    "compiler_version": "g++ (Ubuntu 11.2.0-...) 11.2.0",
    "cmake_version": "3.22.1",
    "glibc_version": "ldd (Ubuntu GLIBC 2.35-...)"
  },
  "config": {
    "cmake_build_type": "Release",
    "cxx_flags_used": "-O3 -march=native -DNDEBUG",
    "toolchain_file": "cmake/toolchains/gcc11.cmake",
    "perf_command": "perf stat -e cycles,instructions ...",
    "gbench_command": "<executable> --benchmark_format=json ..."
  },
  "overrides_applied": { // Content from exp_config.json if used
    "perf_events": ["cache-references", "cache-misses"]
  }
}
```

### 6.5. Data Commits

*   Raw data (`benchmark_output.json`, `perf_stat.log`, `metadata.json`, `assembly/*.s`) stored in `results/` **is intended to be committed** to Git by default.
*   Generated reports and assets in `reports/` are also intended to be committed.
*   Large raw files like `perf.data` or very large datasets generated by benchmarks should typically be `.gitignore`'d. Monitor repository size; consider Git LFS if `results/` becomes excessively large.

---

## 7. Reporting

Reporting is split into two scripts: `generate_report.py` for individual results and `generate_combined_report.py` for summaries and comparisons.

### 7.1. Single Report Generation (`generate_report.py`)

This script transforms the raw results of a *single* experiment run into a human-readable Markdown report.

#### 7.1.1. Report Structure & Assets

*   Reports are generated into `reports/<platform>/<compiler>/<build_flags>/<git_hash>/<experiment_name>/`.
*   Each report directory contains:
    *   `report.md`: The main Markdown file.
    *   `assets/`: A subdirectory holding figures (`.png`, `.svg`), data files (`.csv`), or other artifacts generated specifically for this report instance by `pre_report.py`.

#### 7.1.2. `pre_report.py` Integration

*   If an experiment has an optional `experiments/<experiment_name>/pre_report.py` script:
    *   `generate_report.py` executes it before processing the template for that specific result.
    *   It's called like: `python experiments/exp_A/pre_report.py --results-dir <results/.../exp_A> --output-dir <reports/.../exp_A/assets/>`
    *   This script is responsible for reading data from the results directory and saving any generated files (plots, processed data) into the provided `assets/` directory using **predictable filenames**.

#### 7.1.3. Template Placeholders (`README.md.template`)

The `experiments/<experiment_name>/README.md.template` uses placeholders which `generate_report.py` replaces. The general syntax is `{{TYPE:SPECIFIER}}` or `{{TYPE}}`.

*   **Metadata:**
    *   `{{METADATA_TABLE}}`: Inserts a pre-formatted Markdown table summarizing key info from `metadata.json`.
    *   `{{METADATA:<field_path>}}`: Inserts the value of a specific field from `metadata.json`. Use dot notation for nested fields (e.g., `{{METADATA:environment.cpu_info}}`, `{{METADATA:config.cxx_flags_used}}`).
*   **Google Benchmark:**
    *   `{{GBENCH_TABLE}}`: Inserts a pre-formatted Markdown table summarizing benchmark results from `benchmark_output.json` (e.g., name, time, stddev).
    *   `{{GBENCH_JSON}}`: Inserts the raw JSON content within a ` ```json ... ``` ` block.
*   **Perf:**
    *   `{{PERF_SUMMARY}}`: Inserts a pre-formatted summary of key counters from `perf_stat.log`.
    *   `{{PERF_LOG}}`: Inserts the raw `perf_stat.log` content within a ` ``` ... ``` ` block.
*   **Assembly:**
    *   `{{ASSEMBLY:<FunctionName>}}`: Inserts the assembly code snippet for the specified function (matching a filename like `<FunctionName>.s`) from `results/.../assembly/` within a ` ```asm ... ``` ` block. The `<FunctionName>` should match the base name of the `.s` file (without the extension).
    *   `{{ASSEMBLY_LINKS}}`: Inserts Markdown links to all `.s` files found in the `results/.../assembly/` directory.
*   **Generated Assets (from `pre_report.py`):** These placeholders find files in the corresponding `reports/.../assets/` directory.
    *   `{{FIGURES:<glob_pattern>}}`: Finds all files matching the glob pattern (e.g., `*_plot.png`, `timing*.svg`) in the `assets/` directory and inserts Markdown image links (`![filename](assets/filename)\n`) for each.
    *   `{{ASSETS:<glob_pattern>}}`: Finds all files matching the glob pattern (e.g., `*.csv`, `processed_*.dat`) in the `assets/` directory and inserts Markdown links (`[filename](assets/filename)\n`) for each.
    *   `{{FIGURE:<exact_filename>}}`: Inserts a Markdown image link for one specific file (`![exact_filename](assets/exact_filename)`). Requires `pre_report.py` to generate that exact filename.
    *   `{{ASSET:<exact_filename>}}`: Inserts a Markdown link for one specific file (`[exact_filename](assets/exact_filename)`).

#### 7.1.4. Handling Failures

If `generate_report.py` encounters errors while processing a result:

*   **`pre_report.py` Fails:** Logs the error, continues processing the template, and inserts a marker like `[FIGURE GENERATION FAILED: See console log]` where related `{{FIGURES:*}}` or `{{ASSETS:*}}` placeholders were.
*   **Data Parsing Fails (JSON, Perf Log):** Logs the error, continues, and inserts a marker like `[Data Parsing Failed: Invalid JSON]` or `[Perf Data Unavailable]` where related placeholders (`{{GBENCH_TABLE}}`, `{{PERF_SUMMARY}}`, etc.) were.
*   **Assembly Snippet Missing:** Logs the error, inserts `[Assembly Snippet Not Found: FunctionName]` for `{{ASSEMBLY:FunctionName}}`.
*   **Specific Asset Missing:** Logs the error, inserts `[Asset Not Found: specific_name.png]` for `{{FIGURE:specific_name.png}}` or `{{ASSET:specific_name.csv}}`.

The goal is to produce as much of the report as possible while clearly indicating missing or failed sections.

### 7.2. Combined Report Generation (`generate_combined_report.py`)

This script aggregates data from multiple results to create summary or comparison reports.

#### 7.2.1. Report Types (Summary, Comparison)

Controlled via `generate_combined_report.py --type <type>`:

*   `summary`: Generates a single file (e.g., `ALL_EXPERIMENTS_SUMMARY.md`) within a specific configuration directory (`reports/.../<git_hash>/`), summarizing key metrics across *all experiments* run for that config/hash. It reads data from multiple `results/.../<exp_name>` directories under that specific config/hash path.
*   `comparison`: Generates reports in a dedicated `reports/comparisons/` directory. Requires additional filters to specify *which* results to compare (e.g., `--compare-configs <config1>,<config2>`, `--compare-hashes <hash1>,<hash2>`, potentially limited to specific experiments via `--experiments`). It reads data from multiple `results` directories (potentially across different configs/hashes), performs comparisons (e.g., calculating speedup/slowdown percentages), generates *new* comparative plots/tables, and populates a comparison-specific template.

#### 7.2.2. Comparison Assets

When generating comparison reports, `generate_combined_report.py` may create new assets (plots comparing performance across configurations, tables showing percentage differences). These assets are typically saved within the `reports/comparisons/assets/<comparison_name>/` directory to keep them separate from single-run assets.

#### 7.2.3. Templates for Combined Reports

`generate_combined_report.py` will likely use different, dedicated template files (e.g., stored in `scripts/templates/`) for summary and comparison reports, as the structure and required data differ significantly from the single-experiment template (`README.md.template`). These templates would use placeholders populated with aggregated or calculated data.

### 7.3. Godbolt Integration

Direct automatic link generation is complex. The recommended approach is to include the necessary information in the report template:

### Assembly for BM_MyFunction

Compiler: {{METADATA:config.compiler_version}}
Flags: `{{METADATA:config.cxx_flags_used}}`

```cpp
// Optional: Include C++ source snippet here
void BM_MyFunction(...) { ... }
```

```asm
{{ASSEMBLY:BM_MyFunction}}
```

[View on Godbolt (Manual Setup Required)](https://godbolt.org/)
*(Copy the C++ snippet, select the compiler version, and add the flags above in Godbolt)*

---

## 8. Extensibility Guide

The project is designed to be extended:

### 8.1. Adding a New Profiler (e.g., Valgrind Cachegrind)

1.  **Modify `run_benchmarks.py`:**
    *   Add logic to optionally wrap the benchmark execution with the new tool (`valgrind --tool=cachegrind --cachegrind-out-file=<path> ...`).
    *   Add configuration options (e.g., `--enable-cachegrind`, Cachegrind-specific flags).
    *   Ensure output is saved to the correct `results/.../<exp_name>/` directory.
2.  **Modify `generate_report.py`:**
    *   Add code to parse the new tool's output file (e.g., `cachegrind.out.<pid>`) for the *single* result being processed.
3.  **Modify `experiments/<exp_name>/README.md.template`:**
    *   Define and use new placeholders (e.g., `{{CACHEGRIND_SUMMARY}}`).
4.  **Update `generate_report.py`:** Implement logic to populate the new placeholders.
5.  **(Optional) Modify `generate_combined_report.py`:** If you want to summarize or compare the new profiler's data across runs, update this script to aggregate the relevant data and potentially add new placeholders/sections to the summary/comparison templates.

### 8.2. Adding Custom Analysis/Plots

1.  Create/edit the `experiments/<experiment_name>/pre_report.py` script. (For single-run analysis/plots)
2.  Add Python dependencies (e.g., `matplotlib`, `pandas`, `numpy`) to `scripts/requirements.txt` and install them (`pip install -r scripts/requirements.txt`).
3.  Implement the analysis logic in `pre_report.py` to read data from the `--results-dir` and save generated files (plots, CSVs) to the `--output-dir` using predictable names.
4.  Use corresponding pattern placeholders (`{{FIGURES:*.png}}`, `{{ASSETS:*.csv}}`) in the `experiments/<exp_name>/README.md.template`.
5.  **(Optional) Modify `generate_combined_report.py`:** If you need analysis or plots that compare *multiple* runs (e.g., plotting performance trends across commits or compilers), implement this logic directly within `generate_combined_report.py`. This script would read data from multiple result directories, perform the analysis, save combined plots/assets (likely to `reports/comparisons/assets/`), and populate placeholders in the summary/comparison templates.

### 8.3. Supporting New Platforms

1.  **Update `run_benchmarks.py`:**
    *   Add logic to detect the new platform identifier.
    *   Provide alternative commands if tools like `perf` are unavailable (e.g., use different performance counters, or skip that step).
    *   Use platform-specific equivalents for tools like `objdump` if necessary.
2.  **Add CMake Toolchain Files:** Create appropriate toolchain files in `cmake/toolchains/` for the new platform/compiler combination.
3.  **Update `generate_report.py`:** Adapt parsing logic for single reports if output formats differ significantly.
4.  **Update `generate_combined_report.py`:** Adapt aggregation/comparison logic if output formats differ significantly.

---

## 9. Usage

### 9.1. Prerequisites

*   **Git:** For version control.
*   **CMake:** Recent version (e.g., 3.15+).
*   **C++ Compiler:** Supported compiler (GCC, Clang, MSVC) installed and findable.
*   **Python:** Python 3.6+.
*   **Python Packages:** Install dependencies: `pip install -r scripts/requirements.txt`. Consider using a virtual environment (`python -m venv .venv && source .venv/bin/activate`).
*   **Performance Tools:** `perf` (Linux `linux-tools-common` package or similar). Other platform-specific tools if added.
*   **Build Tools:** `make`, `ninja`, or Visual Studio Build Tools depending on CMake generator.

### 9.2. Basic Steps

1.  **Clone:** `git clone <repo_url> BenchEverything`
2.  **Install Deps:** `cd BenchEverything && pip install -r scripts/requirements.txt`
3.  **Add Experiment:** Follow [Section 4.1](#41-add-experiment).
4.  **Configure Run:** Edit `scripts/config/default.yaml` or create a new one and use `python scripts/run_benchmarks.py --config <your_config.yaml> ...`. Specify targets.
5.  **Run Benchmarks:** `python scripts/run_benchmarks.py [options]`
6.  **Generate Single Reports (Optional but Recommended):** `python scripts/generate_report.py --result-dir <path_to_specific_result>` (Repeat for results of interest).
7.  **Generate Combined Reports (Summary/Comparison):** `python scripts/generate_combined_report.py [options]` (e.g., ` --type comparison --compare-configs gcc,clang`)
8.  **Commit Results & Reports:** `git add results/ reports/ && git commit -m "Run benchmarks for config X and generate reports"`

### 9.3. Benchmarking Tips

*   **Quiet System:** Run on a machine with minimal background activity.
*   **Stable Frequency:** Disable CPU frequency scaling or set the CPU governor to `performance` (Linux). `run_benchmarks.py` could potentially include checks/warnings for this.
*   **Thermals:** Be aware of thermal throttling on long runs. Monitor temperatures if necessary.
*   **Repetitions:** Use sufficient repetitions in Google Benchmark (`--benchmark_repetitions=N`) to get stable results.
*   **Isolate:** Benchmark small, focused pieces of code where possible.

---

## 10. Future Considerations

