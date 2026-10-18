# CAD-PINN Souces (`cad-pinn-souces`)

[![arXiv](https://img.shields.io/badge/arXiv-2606.07198-b31b1b.svg)](https://arxiv.org/pdf/2606.07198)

Differentiable framework for optimizing and parameterizing industrial NURBS geometries via neural deformation fields and physics-informed constraints (PINNs).

---

## 📄 Paper

**Constraint-driven Optimization and Parametrization of Industrial NURBS Geometries via Neural Deformation Field**  
F. Tamburlin, G. Canali, G. A. D’Inverno, N. Demo, A. Mola, G. Rozza  
arXiv:2606.07198 (math.NA), 2026.

👉 [https://arxiv.org/pdf/2606.07198](https://arxiv.org/pdf/2606.07198)

---

## 📦 Repository contents

- **`pyiges/`** — modified Python library for reading, writing, and manipulating IGES files (NURBS).
- **`kvlcc2m.iges`** — example CAD geometry: modified KVLCC2 hull used in the paper experiments.
- **`LICENCE`** — MIT license.

---

## 🚀 What it does

This code allows you to:

- Deform control points of multi-patch NURBS surfaces while preserving CAD connectivity and validity.
- Propagate gradients from the loss to control points end-to-end, without adjoint equations.
- Evaluate differentiable integral quantities on the parametric domain (displaced volume, wetted area, center of buoyancy).
- Export optimized geometries to IGES, ready for downstream industrial pipelines.

---

## 📬 Contact

- **Federico Tamburlin** — [federico.tamburlin@gmail.com](mailto:federico.tamburlin@gmail.com)
- Or open a GitHub Issue for general questions.

## 📝 License

MIT — see [`LICENCE`](https://github.com/fedetamburlin/cad-pinn-souces/blob/main/LICENCE).
