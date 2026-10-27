"""Read-only disassembly triage for local reverse-engineering artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections.abc import Iterator

PROFILE = 'disassembly'
MATCHED_SUFFIXES = frozenset(['.asm', '.dll', '.elf', '.exe', '.lst', '.map', '.objdump', '.pdb', '.s', '.sym'])


def matches(path: Path) -> bool:
    """Return whether a path has an extension relevant to this profile."""
    return path.suffix.lower() in MATCHED_SUFFIXES


def scan(root: Path) -> Iterator[Path]:
    """Yield candidate files without opening or executing them."""
    for path in sorted(root.rglob("*")):
        if path.is_file() and matches(path):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="directory containing local artifacts")
    args = parser.parse_args()
    for path in scan(args.root):
        print(json.dumps({"profile": PROFILE, "path": str(path), "suffix": path.suffix.lower()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
