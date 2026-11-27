"""Pack one real Cerebel session (GEM-X joints + OpenSim IK) into a small JSON for the SVG generator.

usage: python prep_motion.py soma.npz ik.mot out.json
"""
import json, sys
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

z = np.load(sys.argv[1])
J = z['joints_opensim']                          # (T, 77, 3), metres, y up
T, N, _ = J.shape
d = np.linalg.norm(J[:, :, None] - J[:, None], axis=-1)
Wt = d.mean(0) + 8 * d.std(0) + 1e-6             # bones keep their length
np.fill_diagonal(Wt, 0)
edges = np.argwhere(minimum_spanning_tree(Wt).toarray() > 0).tolist()

deg = np.bincount(np.array(edges).ravel(), minlength=N)
leaves = np.where(deg == 1)[0]
motion = np.linalg.norm(np.diff(J, axis=0), axis=-1).sum(0)
trail = [int(i) for i in leaves[np.argsort(-motion[leaves])][:3]]

txt = open(sys.argv[2]).read().split('endheader')[1].strip().splitlines()
hdr = txt[0].split(); data = np.array([l.split() for l in txt[1:]], float)
cols = ['lumbar_bending', 'neck_rotation', 'elbow_flex_r', 'arm_flex_l']
ik = {c: np.round(data[:, hdr.index(c)], 2).tolist() for c in cols}

json.dump(dict(fps=float(z['fps'][0]), joints=np.round(J, 4).tolist(), edges=edges, trail=trail,
               ik_time=np.round(data[:, 0], 4).tolist(), ik=ik), open(sys.argv[3], 'w'))
print('frames', T, 'joints', N, 'edges', len(edges), 'trail', trail, 'ik rows', len(data))
