# CAD-PINN sources

Code accompanying the paper **"Constraint-driven optimization and parametrization of
industrial NURBS geometries via neural deformation field"**, *Computer Methods in
Applied Mechanics and Engineering* **464** (2027) 119500.

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.cma.2026.119500-blue)](https://doi.org/10.1016/j.cma.2026.119500)
[![arXiv](https://img.shields.io/badge/arXiv-2606.07198-b31b1b.svg)](https://arxiv.org/abs/2606.07198)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Differentiable framework for optimizing and parameterizing industrial CAD
geometries represented by multi-patch NURBS surfaces, via neural deformation
fields and physics-informed constraints (PINNs).

> **What is included.** This repository contains the modified `pyiges` library
> used to read, write and manipulate IGES/NURBS geometries, plus the modified
> KVLCC2 hull used in the paper experiments. The optimization and PINN training
> pipeline is **not** included, due to institutional and industrial constraints;
> the method is fully described in the paper (reference [29] points here).

## Repository contents

| Path | Description |
| --- | --- |
| `pyiges/` | Modified [pyiges](https://github.com/pyvista/pyiges) library for IGES/NURBS geometries |
| `kvlcc2m.iges` | Modified KVLCC2 hull used in the paper experiments |
| `examples/read_kvlcc2.py` | Minimal example: read the hull and report mesh statistics |
| `CITATION.cff` | Citation metadata for the GitHub "Cite this repository" button |

## What the library does

- Reads and writes IGES files, including multi-patch NURBS surfaces.
- Deforms control points while preserving CAD connectivity and validity.
- Propagates gradients from the loss to control points end to end, without
  adjoint equations.
- Evaluates differentiable integral quantities on the parametric domain
  (displaced volume, wetted area, center of buoyancy).
- Exports geometries to IGES and tessellated VTK meshes for downstream
  industrial pipelines.

## Install

Requires Python 3.10 or newer.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[full]"
```

The `full` extra installs the optional mesh dependencies (`geomdl`, `pyvista`,
`vtk`). Without them the library still reads and writes IGES, but cannot
tessellate.

## Quick start

```bash
python examples/read_kvlcc2.py
```

```python
import pyiges

iges = pyiges.read("kvlcc2m.iges")
print(iges)                 # Number of Entities: 138
mesh = iges.to_vtk()        # pyvista.PolyData
print(mesh.n_points, mesh.n_cells, mesh.area)
```

## Citation

If you use this code, please cite the paper:

```bibtex
@article{tamburlin2027constraint,
  title   = {Constraint-driven optimization and parametrization of industrial
             NURBS geometries via neural deformation field},
  author  = {Tamburlin, Federico and Canali, Giovanni and D'Inverno, Giuseppe Alessio
             and Demo, Nicola and Mola, Andrea and Rozza, Gianluigi},
  journal = {Computer Methods in Applied Mechanics and Engineering},
  volume  = {464},
  pages   = {119500},
  year    = {2027},
  doi     = {10.1016/j.cma.2026.119500},
  note    = {Preprint: arXiv:2606.07198}
}
```

## Contact

Federico Tamburlin, [federico.tamburlin@gmail.com](mailto:federico.tamburlin@gmail.com).
For questions about the code, please open an issue.

## License

MIT, see [LICENSE](LICENSE). The `pyiges` library is derived from
[pyvista/pyiges](https://github.com/pyvista/pyiges), also MIT-licensed.
