from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
COVER = ROOT / "assets/generated/cover.png"


def main() -> None:
    subprocess.run([sys.executable, "scripts/build_single_index.py"], cwd=ROOT, check=True)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "index.html", DIST / "index.html")
    cover_target = DIST / "assets/generated/cover.png"
    cover_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(COVER, cover_target)
    print(f"wrote {DIST / 'index.html'}")
    print(f"wrote {cover_target}")


if __name__ == "__main__":
    main()
