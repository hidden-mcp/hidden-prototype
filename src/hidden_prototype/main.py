import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hidden_prototype")

HOME_DIR = Path.home()
PROTO_ROOT = (HOME_DIR / ".hidden_prototype").resolve()
PROTO_ROOT.mkdir(exist_ok=True)


@mcp.tool()
def forge_and_run(code: str, purpose: str) -> str:
    """
    Synthesize a standalone Python prototype in an isolated directory and execute it immediately.

    This tool enables an autonomous 'Generate-Execute-Analyze' loop. It creates a dedicated
    workspace for each request to ensure environment isolation and prevent side effects
    between different prototyping tasks.

    Args:
        code (str): The complete Python source code to be executed.
            - Requirements: Must be self-contained.
            - Dependency Management: Use PEP 723 (Inline Script Metadata) format to specify
              external libraries (e.g., `# /// script \n# dependencies = ["requests"] \n# ///`).
            - Output Handling: Scripts should utilize the 'PROTOTYPE_OUTPUT_DIR' environment
              variable to save any generated artifacts (CSV, plots, logs, etc.).
        purpose (str): A concise description of the prototype's objective.
            - Usage: This string is sanitized and used as part of the directory name for
              traceability and workspace isolation.

    Returns:
        str: A detailed execution report including the workspace path, process exit code,
             standard output (stdout), standard error (stderr), and a list of any
             generated artifacts in the output directory.

    Notes:
        - The working directory (CWD) is automatically set to the created prototype folder.
        - Execution is governed by a 180-second timeout to prevent runaway processes.
        - Use this tool to validate hypotheses, perform data analysis, or automate
          local system tasks.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_purpose = "".join(c for c in purpose if c.isalnum() or c in (" ", "_")).replace(" ", "_")[:30]

    proto_dir = PROTO_ROOT / f"{timestamp}_{safe_purpose}"
    output_dir = proto_dir / "outputs"

    proto_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    script_path = (proto_dir / "script.py").resolve()
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

    uv_path = shutil.which("uv")
    if not uv_path:
        return "❌ Error: 'uv' executable not found in PATH."

    env = os.environ.copy()
    env["PROTOTYPE_OUTPUT_DIR"] = str(output_dir.absolute())

    try:
        result = subprocess.run(
            [uv_path, "run", str(script_path)],
            capture_output=True,
            text=True,
            env=env,
            timeout=180,
            cwd=str(proto_dir.absolute()),
        )

        report = [
            f"🚀 Prototype Directory Created: {proto_dir}",
            f"📊 Status: {'Success' if result.returncode == 0 else 'Failed (Exit Code: ' + str(result.returncode) + ')'}",
            "\n[Standard Output]",
            result.stdout or "(No output)",
        ]

        if result.stderr:
            report.append(f"\n[Standard Error]\n{result.stderr}")

        artifacts = list(output_dir.glob("*"))
        if artifacts:
            report.append(f"\n📁 Generated Artifacts in outputs/: {[a.name for a in artifacts]}")

        return "\n".join(report)

    except subprocess.TimeoutExpired:
        return "❌ Error: Execution timed out (180s)."
    except Exception as e:
        return f"❌ System Error: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
