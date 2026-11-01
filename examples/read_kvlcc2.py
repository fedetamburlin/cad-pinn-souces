"""Read the KVLCC2 hull used in the paper and report basic mesh statistics.

Run from any directory after installing the package:

    python examples/read_kvlcc2.py
"""

from pathlib import Path

import pyiges

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    iges = pyiges.read(ROOT / "kvlcc2m.iges")
    print(f"Entities: {len(iges)}")

    mesh = iges.to_vtk()
    print(f"Mesh: {mesh.n_points} points, {mesh.n_cells} cells")
    print(f"Bounds: {[round(value, 3) for value in mesh.bounds]}")
    print(f"Surface area: {mesh.area:.3f}")


if __name__ == "__main__":
    main()
