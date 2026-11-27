# Figure generator

`python tools/gen2.py out/` writes every figure in a light and a dark variant.

Some figures are built from private project data that is not in this repository:

- `render_glasses.py`: renders the glasses CAD (GLB) to the PNGs embedded in the glasses figure.
- `render_msk.py`: renders one OpenSim session (bone meshes + per-frame body poses + muscle paths) to WebP frames.
- `prep_motion.py`, `prep_tennis.py`: pack one GEM-X / OpenSim session and one Tennis AI session into JSON.

Musculoskeletal model: Rajagopal et al. 2016; Lai et al. 2017; Uhlrich et al. 2022 (OpenSim model repository).
