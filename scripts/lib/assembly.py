import subprocess
import re
import os
from pathlib import Path
import platform
from typing import List, Tuple, Dict
import shutil

from .logger import get_logger

logger = get_logger()

class AssemblyExtractor:
    """Extracts assembly code for benchmark functions. (Identical logic to original run_benchmarks.py)"""

    def __init__(self, build_dir: Path, experiment_name: str, benchmark_executable_name: str, project_root: Path):
        self.build_dir = build_dir
        self.experiment_name = experiment_name
        self.benchmark_executable_name = benchmark_executable_name
        self.project_root = project_root
        self.benchmark_exe_path = self.build_dir / "experiments" / self.experiment_name / self.benchmark_executable_name
        self.is_macos = platform.system() == 'Darwin'
        # Store experiment details needed by helper functions originally taking 'experiment' dict
        self.experiment_details = {"name": experiment_name, "benchmark_executable": benchmark_executable_name}

    # ========================================================================
    # Main Public Method (Entry Point) - Mirrors original extract_assembly
    # ========================================================================
    def extract_assembly(self, output_dir: Path, build_flags_id: str):
        """Extract assembly for benchmark functions with source code mapping."""
        logger.info(f"Extracting assembly for {self.experiment_name}...") # Use self.experiment_name

        # Create assembly directory within the output_dir
        assembly_dir = output_dir / "assembly"
        os.makedirs(assembly_dir, exist_ok=True)

        # Get the benchmark executable path (already calculated in __init__)
        benchmark_exe = self.benchmark_exe_path
        if not benchmark_exe.exists():
            logger.error(f"Benchmark executable not found: {benchmark_exe}")
            return # Match original behavior (return without error)

        # --- Mirroring original extract_assembly function ---
        # 1. Find benchmark functions (using original helpers)
        # Try to get benchmark functions from nm first (more reliable)
        benchmark_functions_nm, name_mapping = self._get_benchmark_functions_nm_mapping(benchmark_exe) # Pass benchmark_exe

        # If that fails, fall back to the original method
        if not benchmark_functions_nm:
            logger.info("Could not get benchmark functions from nm, falling back to --benchmark_list_tests")
            # Pass self.experiment_details to mimic original 'experiment' dict
            benchmark_functions_list = self._get_benchmark_functions(benchmark_exe, self.experiment_details)
            benchmark_functions = benchmark_functions_list
            # Use identity mapping if nm failed
            name_mapping = {fname: fname for fname in benchmark_functions_list}
        else:
            benchmark_functions = benchmark_functions_nm # Use the (potentially cleaner) names from nm

        if not benchmark_functions:
            logger.warning(f"No benchmark functions found for {self.experiment_name}")
            (assembly_dir / "_no_functions_found.txt").touch() # Add marker like before
            return # Match original behavior

        # 2. Get source files
        source_files = self._get_source_files(self.experiment_details) # Pass experiment dict

        # 3. Determine if debug info is likely present
        has_debug_info = "Debug" in build_flags_id or "RelWithDebInfo" in build_flags_id

        # 4. Attempt extraction strategies (Mirroring original flow)
        try:
            if has_debug_info:
                # Try to extract assembly with source interleaving for builds with debug info
                if self.is_macos:
                    # For macOS Debug or RelWithDebInfo builds, run dsymutil first
                    self._run_dsymutil(benchmark_exe) # Pass benchmark_exe

                # Try to extract assembly with objdump and debug info
                # Pass necessary args to the helper
                success = self._extract_with_objdump(benchmark_exe, benchmark_functions, assembly_dir, has_debug_info, name_mapping)

                if not success:
                    logger.info("Objdump extraction with debug info failed, falling back to manual extraction")
                    self._manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)
            else:
                # For Release builds without debug info, use manual extraction
                logger.info("Release build without debug info, using manual assembly extraction")
                self._manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)

        except Exception as e:
            logger.warning(f"Error extracting assembly: {e}") # Original used warning
            # Fall back to manual extraction as last resort
            logger.info("Using manual assembly extraction as fallback")
            try:
                self._manual_extraction(benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping)
            except Exception as fallback_e:
                 logger.error(f"Fallback manual assembly extraction also failed: {fallback_e}", exc_info=True)
                 (assembly_dir / "_extraction_error.txt").write_text(f"Main Error: {e}\nFallback Error: {fallback_e}")


    # ========================================================================
    # Helper Methods (Copied VERBATIM and Adapted minimally for class context)
    # ========================================================================

    def _get_benchmark_functions_nm_mapping(self, benchmark_exe): # Added self, takes benchmark_exe
        """Get a mapping from benchmark function names to their mangled names using nm."""
        # (Identical logic to original _get_benchmark_functions_nm_mapping)
        try:
            nm_path = shutil.which("nm") # Check if nm exists
            if not nm_path:
                 logger.warning("'nm' command not found.")
                 return [], {}
            # Run nm with demangling to get symbol information
            nm_cmd = [nm_path, "-C", str(benchmark_exe)]
            result = subprocess.run(nm_cmd, capture_output=True, text=True, check=True, timeout=30, errors='ignore') # Added timeout/ignore

            # Parse the output to find benchmark functions
            benchmark_functions = []
            name_mapping = {}  # Maps benchmark names to their fully mangled versions

            for line in result.stdout.splitlines():
                if "BM_" in line:  # Only look at benchmark functions
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        demangled_name = parts[2]
                        # Extract just the function name part for our benchmark functions
                        if demangled_name.startswith("void BM_"):
                            # Remove the "void " prefix and anything after the function signature
                            func_sig = demangled_name.split("(")[0][5:]  # Remove "void " and anything after "("

                            # Simplify the name for matching purposes (converts from mangled to clean name)
                            clean_name = func_sig
                            # Replace std::__1:: with std::
                            clean_name = clean_name.replace("std::__1::", "std::")
                            # Remove allocator references
                            clean_name = re.sub(r', std::\w+<[^>]+>\s*>', '>', clean_name)
                            clean_name = clean_name.strip() # Added strip

                            # Add to the list of benchmark functions
                            if clean_name not in name_mapping: # Avoid duplicates from nm output
                                benchmark_functions.append(clean_name)
                                # Save mapping between clean name and demangled name (signature part)
                                name_mapping[clean_name] = func_sig

            return sorted(list(set(benchmark_functions))), name_mapping # Ensure uniqueness and sort
        except Exception as e:
            logger.warning(f"Error getting function names using nm: {e}")
            return [], {}

    def _get_benchmark_functions(self, benchmark_exe, experiment): # Added self, takes benchmark_exe, experiment
        """Get list of benchmark functions."""
        # (Identical logic to original _get_benchmark_functions)
        try:
            # Run the benchmark with --benchmark_list_tests
            list_cmd = [str(benchmark_exe), "--benchmark_list_tests=true"]
            result = subprocess.run(list_cmd, capture_output=True, text=True, check=True, timeout=10) # Added timeout
            benchmark_functions = [line.strip() for line in result.stdout.split('\n') if line.strip()]

            # If no functions found this way, use default functions based on experiment
            if not benchmark_functions:
                benchmark_functions = self._get_default_benchmark_functions(experiment) # Pass experiment
            return benchmark_functions
        except subprocess.SubprocessError as e: # Catch specific error
            logger.warning(f"Failed to list tests via benchmark executable: {e}")
            # Fallback to default function names
            return self._get_default_benchmark_functions(experiment) # Pass experiment
        except Exception as e: # Catch other errors
             logger.warning(f"Error running --benchmark_list_tests: {e}")
             return self._get_default_benchmark_functions(experiment) # Pass experiment


    def _get_default_benchmark_functions(self, experiment): # Added self, takes experiment
        """Get default benchmark function names based on experiment type."""
        # (Identical logic to original _get_default_benchmark_functions)
        # if experiment['name'] == "int_addition":
        #     return ["BM_IntAddition"]
        # elif experiment['name'] == "float_addition":
        #     return ["BM_FloatAddition"]
        # else:
        return []

    def _get_source_files(self, experiment): # Added self, takes experiment
        """Get source files for the experiment."""
        # (Identical logic to original _get_source_files)
        source_files = {}
        # Use self.project_root and experiment name
        source_dir = self.project_root / "experiments" / experiment['name'] / "src"
        if not source_dir.is_dir(): return {} # Added check
        # Original used glob, changed to rglob to match previous refactor attempt (more robust)
        for source_file in source_dir.rglob("*.cpp"):
            try:
                # Added encoding and error handling, normalize line endings
                with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
                    source_files[source_file.name] = f.read().replace('\r\n', '\n').replace('\r', '\n')
            except Exception as e:
                logger.warning(f"Could not read source file {source_file}: {e}")
        return source_files

    def _run_dsymutil(self, benchmark_exe): # Added self, takes benchmark_exe
        """Run dsymutil to generate debug symbols (macOS specific)."""
        # (Identical logic to original _run_dsymutil)
        if not self.is_macos: return False # Use self.is_macos
        dsymutil_path = shutil.which("dsymutil") # Check path
        if not dsymutil_path:
            logger.warning("dsymutil command not found.")
            return False
        try:
            logger.info(f"Running dsymutil to generate debug symbols for {benchmark_exe}")
            dsymutil_cmd = [dsymutil_path, str(benchmark_exe)]
            subprocess.run(dsymutil_cmd, check=True, capture_output=True, timeout=60) # Added timeout
            return True
        except Exception as e:
            logger.warning(f"Failed to run dsymutil: {e}")
            return False

    def _extract_with_objdump(self, benchmark_exe, benchmark_functions, assembly_dir, has_debug_info, name_mapping=None): # Added self
        """Extract assembly using objdump with appropriate flags."""
        # (Identical logic to original _extract_with_objdump)
        objdump_path = shutil.which("objdump") # Check path
        if not objdump_path:
             logger.error("'objdump' command not found.")
             return False
        try:
            # Build objdump command with appropriate flags
            objdump_flags = ["-d", "--no-show-raw-insn", "-C"]
            if has_debug_info:
                objdump_flags.insert(0, "-S")  # Add source only if debug info is available

            # Add macOS flag if needed (original didn't have this specific check)
            if self.is_macos and shutil.which("llvm-objdump"):
                 # Prefer llvm-objdump on mac if available? Original didn't switch. Sticking to objdump.
                 # objdump_flags.append("--macho") # Might be needed for system objdump on Mach-O
                 pass


            objdump_cmd = [objdump_path] + objdump_flags + [str(benchmark_exe)]
            logger.info(f"Running: {' '.join(objdump_cmd)}")

            result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True, timeout=120, errors='ignore') # Added timeout/ignore
            mixed_assembly = result.stdout

            # Write full mixed assembly for reference
            output_filename = "full_mixed_assembly.txt" if has_debug_info else "full_objdump_output.txt"
            (assembly_dir / output_filename).write_text(mixed_assembly, encoding='utf-8') # Use write_text

            # Extract function-specific assembly
            extracted_count = 0 # Track success
            for func_name in benchmark_functions:
                # If we have name mapping from nm, use it for more precise matching
                lookup_name = name_mapping.get(func_name, func_name) if name_mapping else func_name

                func_asm = self._extract_function_assembly(mixed_assembly, lookup_name, func_name) # Call helper

                if func_asm:
                    outfile = assembly_dir / f"{func_name}.s"
                    try:
                        with open(outfile, "w", encoding='utf-8') as f: # Added encoding
                            f.write("\n".join(func_asm))
                        logger.info(f"Extracted {'mixed source/' if has_debug_info else ''}assembly for {func_name}")
                        extracted_count += 1
                    except Exception as write_err:
                         logger.error(f"Failed to write assembly for {func_name} to {outfile}: {write_err}")
                else:
                    logger.warning(f"Could not find {func_name} in assembly output")
                    (assembly_dir / f"{func_name}.s.missing").touch() # Add marker

            # Return True if subprocess ran ok, even if not all functions found
            return True
        except subprocess.CalledProcessError as e: # More specific error handling
             logger.error(f"Objdump command failed (retcode {e.returncode}). Stderr: {e.stderr[:1000]}...")
             return False
        except subprocess.TimeoutExpired:
             logger.error("Objdump command timed out.")
             return False
        except Exception as e:
            logger.warning(f"Error extracting assembly with objdump: {e}") # Original used warning
            return False

    def _extract_function_assembly(self, assembly_text, lookup_name, original_name=None): # Added self
        """Extract assembly for a specific function from full assembly text."""
        # (Identical logic to original _extract_function_assembly)
        lines = assembly_text.splitlines()
        func_asm = []
        capturing = False

        comment_name = original_name if original_name else lookup_name

        # Try direct match first
        for i, line in enumerate(lines):
            # Look for function start marker (original logic)
            if lookup_name in line and ":" in line:
                 # Add heuristic check for function label format
                 if re.match(r"^[0-9a-f]+\s+<.*" + re.escape(lookup_name) + r".*>:", line) or \
                    re.match(r"^" + re.escape(lookup_name) + r"\(.*\):", line.strip()):
                    capturing = True
                    if original_name and lookup_name != original_name:
                        func_asm.append(f"// Assembly for benchmark function: {original_name} (matched on '{lookup_name}')")
                    else:
                         func_asm.append(f"// Assembly for benchmark function: {comment_name}")
                    func_asm.append(line)
            elif capturing:
                # Look for function end marker (next function label)
                # Original logic: just looked for the next label <...>:.
                if "<" in line and ">:" in line and not line.strip().startswith("."):
                     # Check if it's a *different* function label
                     if lookup_name not in line:
                          capturing = False
                          # Do not append the line starting the next function
                 # Add check for common end directive
                elif line.strip() == ".cfi_endproc":
                     func_asm.append(line)
                     capturing = False
                else:
                    func_asm.append(line)

        # If we didn't find a match but have a template function, try a more flexible approach (Original logic)
        if not func_asm and "<" in lookup_name and ">" in lookup_name:
            base_name = lookup_name.split("<")[0]
            # Reset capturing flag
            capturing = False
            for i, line in enumerate(lines):
                # Look for base_name<...> label
                if base_name in line and "<" in line and ">:" in line:
                    # Make sure this is the right function by checking parts of the template (Original logic)
                    template_parts = re.findall(r'<([^<>]+)>', lookup_name)
                    # Basic check if parts appear in the line
                    if template_parts and all(part in line for part in template_parts):
                        capturing = True
                        if original_name:
                            func_asm.append(f"// Assembly for benchmark function: {original_name} (flexible match)")
                        else:
                             func_asm.append(f"// Assembly for benchmark function: {comment_name} (flexible match)")
                        func_asm.append(line)
                elif capturing:
                    # Same end condition as above
                    if "<" in line and ">:" in line and not line.strip().startswith("."):
                         if lookup_name not in line and base_name not in line: # Check base name too
                              capturing = False
                    elif line.strip() == ".cfi_endproc":
                         func_asm.append(line)
                         capturing = False
                    else:
                        func_asm.append(line)

        return func_asm


    def _manual_extraction(self, benchmark_exe, benchmark_functions, source_files, assembly_dir, name_mapping=None): # Added self
        """Fallback function to extract assembly and manually combine with source."""
        # (Identical logic to original manual_extraction)
        objdump_path = shutil.which("objdump") # Check path
        if not objdump_path:
             logger.error("'objdump' command not found for manual extraction.")
             return
        try:
            # Try with standard objdump to get full disassembly
            objdump_flags = ["-d", "--no-show-raw-insn", "-C"]
            if self.is_macos: # Add check for macOS specific flags if needed
                 pass # Original didn't add --macho here

            objdump_cmd = [objdump_path] + objdump_flags + [str(benchmark_exe)]
            result = subprocess.run(objdump_cmd, capture_output=True, text=True, check=True, timeout=120, errors='ignore') # Added timeout/ignore
            disassembly = result.stdout

            # Write full disassembly for reference
            (assembly_dir / "full_disassembly.txt").write_text(disassembly, encoding='utf-8') # Use write_text

            # Extract function-specific assembly using nm name mapping if available
            lines = disassembly.split('\n')
            extracted_count = 0 # Track success

            for func_name in benchmark_functions:
                 # Skip if already extracted (e.g., by a previous -S attempt)
                 if (assembly_dir / f"{func_name}.s").exists():
                      logger.debug(f"Skipping manual extraction for {func_name}, already exists.") 
                      continue

                 # If we have a name mapping from nm, use the mapped name for lookup
                 lookup_name = name_mapping.get(func_name, func_name) if name_mapping else func_name

                 # For template functions, get the base name for template extraction
                 is_template = '<' in func_name
                 base_name = func_name.split('<')[0] if is_template else func_name

                 # Try with the mapped name from nm first
                 func_asm = self._extract_direct_match(lines, lookup_name, func_name)

                 # If that fails and we don't have a mapping or the mapping didn't help,
                 # fall back to our multi-strategy approach (Original logic)
                 if not func_asm and (not name_mapping or lookup_name == func_name):
                     # Strategy 2: Regex pattern match for C++ templates
                     func_asm = self._extract_template_match(lines, func_name)

                     # Strategy 3: Base name match
                     if not func_asm:
                         func_asm = self._extract_base_name_match(lines, func_name)

                     # Strategy 4: Generic pattern match (most relaxed)
                     if not func_asm:
                         func_asm = self._extract_generic_match(lines, func_name)

                 # Create the assembly file
                 outfile = assembly_dir / f"{func_name}.s"
                 try:
                     with open(outfile, "w", encoding='utf-8') as f: # Added encoding
                         # If it's a template function, extract the template definition
                         if is_template:
                             template_def = self.extract_template_definition(source_files, base_name) # Call self method
                             if template_def:
                                 f.write(f"// Template definition for {base_name}:\n")
                                 f.write("/*\n" + template_def + "\n*/\n\n") # Add comment markers
                             else:
                                 f.write(f"// Could not find template definition for {base_name}\n\n")
                         # For non-template functions, extract the function definition
                         else:
                             func_def = self.extract_function_definition(source_files, base_name)
                             if func_def:
                                 f.write(f"// Function definition for {base_name}:\n")
                                 f.write("/*\n" + func_def + "\n*/\n\n") # Add comment markers
                             else:
                                 f.write(f"// Could not find function definition for {base_name}\n\n")

                         # Include any assembly we found
                         if func_asm:
                             f.write("// Assembly:\n")
                             f.write('\n'.join(func_asm))
                             logger.info(f"Extracted assembly for {func_name} (manual)")
                             extracted_count += 1
                         else:
                             f.write(f"// Note: Assembly for {func_name} could not be found\n")
                             f.write(f"// Look for function containing '{base_name}' in full_disassembly.txt\n")
                             logger.warning(f"Could not find assembly for {func_name} (manual)")
                             # Create missing marker if not found
                             (assembly_dir / f"{func_name}.s.missing").touch()
                 except Exception as write_err:
                      logger.error(f"Failed to write manual assembly for {func_name} to {outfile}: {write_err}")


        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.warning(f"Failed to extract assembly manually: {e}") # Original used warning
        except Exception as e:
             logger.error(f"Unexpected error during manual extraction: {e}", exc_info=True)


    # --- Original Matching Strategy Helpers ---

    def _extract_direct_match(self, lines, lookup_name, original_name=None): # Added self
        """Extract assembly using direct string match."""
        # (Identical logic to original _extract_direct_match)
        func_asm = []
        capturing = False
        comment_name = original_name if original_name else lookup_name
        for line in lines:
            if lookup_name in line and ":" in line:
                 # Add heuristic check for function label format
                 if re.match(r"^[0-9a-f]+\s+<.*" + re.escape(lookup_name) + r".*>:", line) or \
                    re.match(r"^" + re.escape(lookup_name) + r"\(.*\):", line.strip()):
                    capturing = True
                    if original_name and lookup_name != original_name:
                        func_asm.append(f"// Assembly for benchmark function: {comment_name}")
                    func_asm.append(line)
            elif capturing:
                if "<" in line and ">:" in line and not line.strip().startswith("."):
                     if lookup_name not in line: capturing = False
                elif line.strip() == ".cfi_endproc":
                     func_asm.append(line); capturing = False
                else: func_asm.append(line)
        return func_asm

    def _extract_template_match(self, lines, func_name): # Added self
        """Extract assembly using regex matching for C++ templates."""
        # (Identical logic to original _extract_template_match)
        func_asm = []
        capturing = False
        match = re.match(r'([^<]+)(<.*>)?', func_name)
        if not match: return []
        base_name, template_part = match.groups()

        if template_part:
            clean_template = template_part.replace(" ", "")
            template_regex = clean_template.replace('std::', r'std::(?:__1::)?')
            template_regex = re.sub(r'>$', r'(?:,std::(?:__1::)?allocator<[^>]+>)?>', template_regex)
            # Original pattern was quite complex, trying to replicate
            first_template_arg = clean_template.split('<', 1)[1].split('>')[0].split(',')[0]
            pattern_str = re.escape(base_name) + r'<.*' + re.escape(first_template_arg) + r'.*>'
            pattern = re.compile(pattern_str)
        else:
            pattern = re.compile(re.escape(base_name) + r'(?:<.*>)?') # Original fallback

        start_pattern = re.compile(rf"^[0-9a-f]+\s+<.*{pattern.pattern}.*>:") # Look for pattern within <...>
        end_pattern = re.compile(r"^(?:[0-9a-f]+\s+<.*>:)|(?:^[_a-zA-Z].*\(.*\):)")

        for line in lines:
            if capturing:
                if end_pattern.match(line) and not pattern.search(line):
                    capturing = False; break
                else: func_asm.append(line)
            elif start_pattern.search(line):
                capturing = True
                func_asm.append(f"// Best-effort match for {func_name} using template pattern matching:")
                func_asm.append(line)
        return func_asm


    def _extract_base_name_match(self, lines, func_name): # Added self
        """Extract assembly using just the base name of the function."""
        # (Identical logic to original _extract_base_name_match)
        func_asm = []
        capturing = False
        base_name = func_name.split('<')[0] if '<' in func_name else func_name
        escaped_base = re.escape(base_name)

        # Original pattern looked for base_name followed by <...>
        start_pattern = re.compile(rf"^[0-9a-f]+\s+<{escaped_base}<.*>:>")
        end_pattern = re.compile(r"^(?:[0-9a-f]+\s+<.*>:)|(?:^[_a-zA-Z].*\(.*\):)")

        for line in lines:
            if capturing:
                if end_pattern.match(line) and not start_pattern.search(line):
                    capturing = False; break
                else: func_asm.append(line)
            elif start_pattern.search(line):
                capturing = True
                func_asm.append(f"// Possible match for {func_name} using base name {base_name}:")
                func_asm.append(line)
        return func_asm

    def _extract_generic_match(self, lines, func_name): # Added self
        """Generic pattern matching as a last resort."""
        # (Identical logic to original _extract_generic_match)
        func_asm = []
        capturing = False
        template_args = []
        if '<' in func_name and '>' in func_name:
            template_part = func_name[func_name.find('<')+1:func_name.rfind('>')]
            template_args = re.findall(r'std::(\w+)|(\d+)', template_part)
            template_args = [x[0] or x[1] for x in template_args if x[0] or x[1]]

        if template_args:
            base_name = func_name.split('<')[0]
            # Original pattern: address <base_name...arg1...argN...>:
            start_pattern_str = rf"^[0-9a-f]+\s+<{re.escape(base_name)}.*" + ".*".join(re.escape(arg) for arg in template_args) + r".*>:"
            start_pattern = re.compile(start_pattern_str)
            end_pattern = re.compile(r"^(?:[0-9a-f]+\s+<.*>:)|(?:^[_a-zA-Z].*\(.*\):)")

            for line in lines:
                if capturing:
                    if end_pattern.match(line) and not start_pattern.search(line):
                         capturing = False; break
                    else: func_asm.append(line)
                elif start_pattern.search(line):
                    capturing = True
                    func_asm.append(f"// Best-effort match for {func_name} using generic pattern matching:")
                    func_asm.append(line)
        return func_asm


    # --- Source Context Helper ---
    def extract_template_definition(self, source_files, base_func_name): # Added self
        """Extract the template definition for a benchmark function."""
        # (Identical logic to original extract_template_definition)
        for source_file, content in source_files.items():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "template" in line and "<" in line and ">" in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        if j < len(lines) and base_func_name in lines[j]:
                            start_line = i; func_lines = []; brace_count = 0; in_function = False
                            func_lines.append(lines[start_line])
                            k = start_line + 1
                            while k < len(lines) and not in_function:
                                func_lines.append(lines[k])
                                if "{" in lines[k]: in_function = True; brace_count = lines[k].count('{')
                                k += 1
                            while k < len(lines) and in_function:
                                line_k = lines[k] # Use different var name
                                func_lines.append(line_k)
                                brace_count += line_k.count('{')
                                brace_count -= line_k.count('}')
                                if brace_count <= 0: break
                                k += 1
                            return '\n'.join(func_lines)
                elif base_func_name in line and "<" in line and ">" in line and ("{" in line or ";" in line):
                    for j in range(i-1, max(0, i-5), -1):
                        if "template" in lines[j] and "<" in lines[j] and ">" in lines[j]:
                            start_line = j; func_lines = []; brace_count = 0; in_function = False
                            for l in range(start_line, i+1):
                                func_lines.append(lines[l])
                                if "{" in lines[l]: in_function = True; brace_count = lines[l].count('{')
                            if in_function:
                                k = i + 1
                                while k < len(lines) and brace_count > 0:
                                    line_k = lines[k] # Use different var name
                                    func_lines.append(line_k)
                                    brace_count += line_k.count('{')
                                    brace_count -= line_k.count('}')
                                    k += 1
                                return '\n'.join(func_lines)
        return None

    def extract_function_definition(self, source_files, func_name):
        """Extract the function definition for a regular (non-template) benchmark function."""
        for source_file, content in source_files.items():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Look for the function definition (various patterns)
                if re.search(r'\b' + re.escape(func_name) + r'\s*\(', line) and not line.strip().startswith('//'):
                    # Found a potential function definition
                    start_line = i
                    func_lines = []
                    in_function = False
                    brace_count = 0
                    
                    # Check a few lines before to see if there are any comments or annotations
                    for j in range(max(0, i-5), i):
                        if lines[j].strip().startswith('//') or lines[j].strip().startswith('/*') or lines[j].strip().startswith('*'):
                            func_lines.append(lines[j])
                    
                    # Add the function signature line
                    func_lines.append(lines[start_line])
                    
                    # Check if the function signature is followed by an opening brace
                    if '{' in lines[start_line]:
                        in_function = True
                        brace_count = lines[start_line].count('{')
                    
                    # If not, look for the opening brace in subsequent lines
                    k = start_line + 1
                    while k < len(lines) and not in_function:
                        func_lines.append(lines[k])
                        if '{' in lines[k]:
                            in_function = True
                            brace_count = lines[k].count('{')
                        k += 1
                    
                    # Continue adding lines until the function ends (brace count reaches 0)
                    while k < len(lines) and in_function:
                        line_k = lines[k]
                        func_lines.append(line_k)
                        brace_count += line_k.count('{')
                        brace_count -= line_k.count('}')
                        if brace_count <= 0:
                            break
                        k += 1
                    
                    # If we found a complete function, return it
                    if brace_count <= 0:
                        return '\n'.join(func_lines)
        
        return None