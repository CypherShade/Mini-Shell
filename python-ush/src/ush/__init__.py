"""
Package initializer for the python-ush project.

Provides a minimal public API:
- VERSION: package version string
- run(argv=None): entry point to run interactive REPL or a script file
"""
from __future__ import annotations

import os
from typing import Iterable, Optional

__all__ = ["VERSION", "run"]

VERSION = "0.1.0"


def _import_core():
    """
    Import the core module (src/ush/ush.py). Raise an informative ImportError
    if the core implementation is missing or fails to import.
    """
    try:
        from . import ush as _core  # relative import of the main implementation
        return _core
    except Exception as exc:  # keep broad to surface import/runtime errors inside core
        raise ImportError(
            "Could not import core module 'ush'. Ensure 'src/ush/ush.py' exists and is importable."
        ) from exc


def run(argv: Optional[Iterable[str]] = None) -> int:
    """
    Run the shell.

    - If argv is provided and the first element is an existing file path, attempt to run that
      file in non-interactive/script mode (delegates to core.run_script or core.main).
    - Otherwise launch the interactive REPL (delegates to core.repl or core.main).

    Returns an integer exit code when possible.
    """
    core = _import_core()

    args = list(argv) if argv else []
    # script execution: first arg is an existing file
    if args:
        first = args[0]
        if isinstance(first, str) and os.path.exists(first):
            # Prefer explicit run_script, fallback to main(argv)
            if hasattr(core, "run_script"):
                return core.run_script(first, args[1:]) or 0
            if hasattr(core, "main"):
                return core.main([first] + args[1:]) or 0

    # interactive mode
    if hasattr(core, "repl"):
        core.repl()
        return 0
    if hasattr(core, "main"):
        return core.main([]) or 0

    raise RuntimeError("Core module provides no entrypoint (repl/run_script/main).")