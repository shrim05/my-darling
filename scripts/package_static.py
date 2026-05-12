from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def main() -> None:
    subprocess.run([sys.executable, "scripts/build_single_index.py"], cwd=ROOT, check=True)
    DIST.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "index.html", DIST / "index.html")
    print(f"wrote {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
