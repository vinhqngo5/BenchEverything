import re
import json
from pathlib import Path
from typing import Dict, Optional, List

from .logger import get_logger
from .report_utils import (
     create_gbench_table, create_metadata_table, create_assembly_links_section,
     format_path_for_markdown
)

logger = get_logger()

class TemplateRenderer:
    """Renders Markdown report templates by replacing placeholders."""

    def __init__(self, template_path: Path):
        self.template_path = template_path
        self.template_content = self._load_template()

    def _load_template(self) -> Optional[str]:
        """Load the template file content."""
        if not self.template_path or not self.template_path.exists():
            logger.error(f"Template file not found: {self.template_path}")
            return None
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading template file {self.template_path}: {e}")
            return None

    def render(self, context: Dict, report_dir: Path, project_root: Path) -> Optional[str]:
        """
        Replace placeholders in the template with data from the context.

        Args:
            context: Dictionary containing data for placeholders. Expected keys:
                     'gbench_data', 'metadata', 'perf_log', 'assembly_files' (dict path),
                     'experiment_name', etc.
            report_dir: The directory where the report.md file will be saved.
            project_root: The root directory of the project.

        Returns:
            The rendered Markdown string, or None if rendering fails.
        """
        if self.template_content is None:
            return None

        content = self.template_content
        assets_dir = report_dir / "assets" # Assume assets are here

        # --- Standard Placeholders ---
        if '{{GBENCH_TABLE}}' in content:
            gbench_table = create_gbench_table(context.get('gbench_data'))
            content = content.replace('{{GBENCH_TABLE}}', gbench_table)

        if '{{GBENCH_JSON}}' in content:
            gbench_data = context.get('gbench_data')
            json_str = json.dumps(gbench_data, indent=2) if gbench_data else "[No benchmark JSON available]"
            content = content.replace('{{GBENCH_JSON}}', f"```json\n{json_str}\n```")

        if '{{METADATA_TABLE}}' in content:
            metadata_table = create_metadata_table(context.get('metadata'))
            content = content.replace('{{METADATA_TABLE}}', metadata_table)

        if '{{PERF_SUMMARY}}' in content:
             # Basic summary: just include the log content directly for now
             perf_log = context.get('perf_log', "Performance counter data not available.")
             content = content.replace('{{PERF_SUMMARY}}', f"```\n{perf_log}\n```")

        if '{{PERF_LOG}}' in content:
            perf_log = context.get('perf_log', "Performance counter data not available.")
            content = content.replace('{{PERF_LOG}}', f"```\n{perf_log}\n```")

        if '{{ASSEMBLY_LINKS}}' in content:
             assembly_files = context.get('assembly_files', {}) # Dict func_name -> Path
             asm_links_section = create_assembly_links_section(assembly_files, report_dir)
             content = content.replace('{{ASSEMBLY_LINKS}}', asm_links_section)

        # --- Specific Metadata Placeholders: {{METADATA:field.subfield}} ---
        metadata = context.get('metadata', {})
        for match in re.finditer(r'\{\{METADATA:([^}]+)\}\}', content):
            key_path = match.group(1)
            value = metadata
            try:
                for part in key_path.split('.'):
                     if isinstance(value, dict):
                          value = value.get(part, f"METADATA:{key_path} not found")
                     else:
                          value = f"METADATA:{key_path} path invalid"
                          break
                content = content.replace(match.group(0), str(value))
            except Exception as e:
                logger.warning(f"Error resolving metadata placeholder {match.group(0)}: {e}")
                content = content.replace(match.group(0), f"[Error: {key_path}]")

        # --- Specific Assembly Placeholders: {{ASSEMBLY:FunctionName}} ---
        assembly_files = context.get('assembly_files', {})
        for match in re.finditer(r'\{\{ASSEMBLY:([^}]+)\}\}', content):
             func_name = match.group(1)
             asm_path = assembly_files.get(func_name)
             asm_content = f"[Assembly for {func_name} not found]"
             if asm_path and asm_path.exists():
                  try:
                       with open(asm_path, 'r', encoding='utf-8') as f:
                            asm_content = f.read()
                  except Exception as e:
                       logger.error(f"Error reading assembly file {asm_path}: {e}")
                       asm_content = f"[Error reading assembly for {func_name}]"

             content = content.replace(match.group(0), f"\n{asm_content}\n")


        # --- Asset Placeholders (FIGURE, ASSET, FIGURES, ASSETS) ---
        # {{FIGURE:filename.png}}
        for match in re.finditer(r'\{\{FIGURE:([^}]+)\}\}', content):
            filename = match.group(1)
            figure_path = assets_dir / filename
            if figure_path.exists():
                rel_path = format_path_for_markdown(figure_path, report_dir, project_root)
                replacement = f"![{filename}]({rel_path})"
            else:
                replacement = f"[Figure Not Found: {filename}]"
                logger.warning(f"Figure asset not found: {figure_path}")
            content = content.replace(match.group(0), replacement)

        # {{ASSET:filename.csv}}
        for match in re.finditer(r'\{\{ASSET:([^}]+)\}\}', content):
            filename = match.group(1)
            asset_path = assets_dir / filename
            if asset_path.exists():
                rel_path = format_path_for_markdown(asset_path, report_dir, project_root)
                replacement = f"[{filename}]({rel_path})"
            else:
                replacement = f"[Asset Not Found: {filename}]"
                logger.warning(f"Asset not found: {asset_path}")
            content = content.replace(match.group(0), replacement)

        # {{FIGURES:pattern}}
        for match in re.finditer(r'\{\{FIGURES:([^}]+)\}\}', content):
            pattern = match.group(1)
            figures = sorted(list(assets_dir.glob(pattern)))
            replacement = ""
            if figures:
                for fig_path in figures:
                    rel_path = format_path_for_markdown(fig_path, report_dir, project_root)
                    replacement += f"![{fig_path.name}]({rel_path})\n\n"
                replacement = replacement.strip()
            else:
                replacement = f"[No figures found matching '{pattern}']"
                logger.warning(f"No figure assets found matching pattern '{pattern}' in {assets_dir}")
            content = content.replace(match.group(0), replacement)

        # {{ASSETS:pattern}}
        for match in re.finditer(r'\{\{ASSETS:([^}]+)\}\}', content):
            pattern = match.group(1)
            assets = sorted(list(assets_dir.glob(pattern)))
            replacement = ""
            if assets:
                for asset_path in assets:
                    rel_path = format_path_for_markdown(asset_path, report_dir, project_root)
                    replacement += f"- [{asset_path.name}]({rel_path})\n"
                replacement = replacement.strip()
            else:
                replacement = f"[No assets found matching '{pattern}']"
                logger.warning(f"No assets found matching pattern '{pattern}' in {assets_dir}")
            content = content.replace(match.group(0), replacement)

        # {{RELATED_LINKS}} - Simple version linking to experiment source and raw results
        if '{{RELATED_LINKS}}' in content:
             exp_name = context.get('experiment_name', 'unknown_experiment')
             exp_src_path = project_root / "experiments" / exp_name
             results_dir = context.get('results_dir') # Should be passed in context

             links = "## Related Resources\n\n"
             try:
                  rel_exp_path = format_path_for_markdown(exp_src_path, report_dir, project_root)
                  links += f"- [Experiment Source Code]({rel_exp_path})\n"
             except Exception as e:
                  logger.warning(f"Could not create relative link for experiment source {exp_src_path}: {e}")
                  links += f"- Experiment Source Code (Path: {exp_src_path})\n"

             if results_dir:
                  try:
                       rel_res_path = format_path_for_markdown(results_dir, report_dir, project_root)
                       links += f"- [Raw Benchmark Results]({rel_res_path})\n"
                  except Exception as e:
                       logger.warning(f"Could not create relative link for results dir {results_dir}: {e}")
                       links += f"- Raw Benchmark Results (Path: {results_dir})\n"
             else:
                  links += f"- Raw Benchmark Results (Path not available)\n"

             content = content.replace('{{RELATED_LINKS}}', links)


        # --- Cleanup any remaining placeholders ---
        remaining_placeholders = re.findall(r'\{\{[^}]+\}\}', content)
        if remaining_placeholders:
             logger.warning(f"Unresolved placeholders remaining in report for {context.get('experiment_name')}: {remaining_placeholders}")
             # Optionally replace them with a warning message
             # for ph in remaining_placeholders:
             #     content = content.replace(ph, f"[Unresolved Placeholder: {ph}]")

        return content