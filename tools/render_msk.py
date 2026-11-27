"""Render one real OpenSim session (Rajagopal bones + 80 muscle paths) to WebP frames.

usage: python render_msk.py bones.glb opensim-motion.json outdir [step]
"""
import json, math, os, sys
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFilter

glb, motion, out = sys.argv[1], sys.argv[2], sys.argv[3]
STEP = int(sys.argv[4]) if len(sys.argv) > 4 else 3
W, H, SS = 380, 560, 2
os.makedirs(out, exist_ok=True)

M = json.load(open(motion))
scale = M['metadata'].get('visualScale', 1.0)
scene = trimesh.load(glb)
bones = {}
for node in scene.graph.nodes_geometry:
    T, g = scene.graph[node]
    m = scene.geometry[g].copy(); m.apply_transform(T)
    if len(m.faces) > 4000:
        m = m.simplify_quadric_decimation(face_count=4000)
    bones[node] = (np.asarray(m.vertices) * scale, np.asarray(m.faces))
print('bones', len(bones), sum(len(f) for _, f in bones.values()), 'faces')

def qrot(q, v):
    x, y, z, w = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    return v @ R.T

frames = M['frames'][::STEP]
pel = np.array([f['pelvis'] for f in M['frames']])
cx, cz = pel[:, 0].mean(), pel[:, 2].mean()
YAW, PITCH, DIST = math.radians(-35), math.radians(8), 4.0

def cam(P):
    x, y, z = P[..., 0] - cx, P[..., 1] - .92, P[..., 2] - cz
    x2 = x * math.cos(YAW) - z * math.sin(YAW); z2 = x * math.sin(YAW) + z * math.cos(YAW)
    y3 = y * math.cos(PITCH) - z2 * math.sin(PITCH); z3 = y * math.sin(PITCH) + z2 * math.cos(PITCH)
    return np.stack([x2, y3, z3], -1)

F = 960
def proj(C):
    d = DIST - C[..., 2]
    return np.stack([(W / 2 + F * C[..., 0] / d) * SS, (H * .57 - F * C[..., 1] / d) * SS], -1), d

key = np.array([-.45, .7, .55]); key /= np.linalg.norm(key)
fill = np.array([.6, .1, .5]); fill /= np.linalg.norm(fill)
THEMES = {
    'light': dict(bone_lo=(150, 140, 118), bone_hi=(250, 246, 236), mus=(178, 58, 48), mus_hi=(236, 140, 120), grid=(208, 215, 222, 255), shadow=(0, 0, 0, 40)),
    'dark': dict(bone_lo=(96, 92, 84), bone_hi=(236, 230, 214), mus=(196, 70, 58), mus_hi=(240, 135, 112), grid=(48, 54, 61, 255), shadow=(0, 0, 0, 90)),
}
names = []
for k, fr in enumerate(frames):
    items = []   # (depth, kind, data)
    for bname, (V, Fc) in bones.items():
        b = fr['bodies'].get(bname)
        if b is None: continue
        Pw = qrot(b['q'], V) + np.array(b['p'])
        C = cam(Pw); XY, d = proj(C)
        n = np.cross(C[Fc[:, 1]] - C[Fc[:, 0]], C[Fc[:, 2]] - C[Fc[:, 0]])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        n *= np.where(n[:, 2:3] < 0, -1, 1)
        lam = np.clip(n @ key, 0, 1) * .8 + np.clip(n @ fill, 0, 1) * .25 + .08
        fd = d[Fc].mean(1)
        for i in range(len(Fc)):
            a, bb, c = Fc[i]
            items.append((fd[i], 0, (tuple(XY[a]), tuple(XY[bb]), tuple(XY[c])), lam[i]))
    for mu in fr['muscles']:
        P = np.array(mu['points']); C = cam(P); XY, d = proj(C)
        for i in range(len(P) - 1):
            items.append(((d[i] + d[i + 1]) / 2 - .02, 1, (tuple(XY[i]), tuple(XY[i + 1])), (d[i] + d[i + 1]) / 2))
    items.sort(key=lambda t: -t[0])
    for tname, th in THEMES.items():
        img = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); dr = ImageDraw.Draw(img)
        # floor grid and contact shadow
        for g in np.arange(-1.0, 1.01, .25):
            for a, b in (((cx + g, 0, cz - 1), (cx + g, 0, cz + 1)), ((cx - 1, 0, cz + g), (cx + 1, 0, cz + g))):
                p, _ = proj(cam(np.array([a, b])))
                dr.line([tuple(p[0]), tuple(p[1])], fill=th['grid'], width=SS)
        feet = np.array([fr['bodies'][n_]['p'] for n_ in ('calcn_r', 'calcn_l', 'pelvis')]); feet[:, 1] = 0
        fp, _ = proj(cam(feet))
        sh = Image.new('L', img.size, 0); sd = ImageDraw.Draw(sh)
        cxs, cys = fp[:, 0].mean(), fp[:, 1].mean()
        sd.ellipse([cxs - 70 * SS, cys - 16 * SS, cxs + 70 * SS, cys + 16 * SS], fill=th['shadow'][3])
        sh = sh.filter(ImageFilter.GaussianBlur(12 * SS))
        img.paste(Image.new('RGBA', img.size, th['shadow'][:3] + (255,)), (0, 0), sh)
        dr = ImageDraw.Draw(img)
        lo, hi = np.array(th['bone_lo']), np.array(th['bone_hi'])
        for depth, kind, geo, val in items:
            if kind == 0:
                col = tuple(int(v) for v in lo + (hi - lo) * min(1, val)) + (255,)
                dr.polygon(geo, fill=col, outline=col)
            else:
                w = max(2, int(SS * 15 / val))
                dr.line(geo, fill=th['mus'] + (235,), width=w)
                dr.line(geo, fill=th['mus_hi'] + (150,), width=max(1, w // 3))
                for p in geo:
                    dr.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=th['mus'] + (235,))
        img = img.resize((W, H), Image.LANCZOS)
        fn = f'{out}/msk-{tname}-{k:03d}.webp'
        img = img.resize((250, 368), Image.LANCZOS); img.save(fn, "WEBP", quality=52, alpha_quality=35, method=6)
    names.append(k)
    if k % 10 == 0: print('frame', k, '/', len(frames))
json.dump(dict(n=len(names), fps=M['frames'][1]['time'] and 1 / (M['frames'][1]['time'] - M['frames'][0]['time']) / STEP,
               duration=M['frames'][-1]['time'], meta=M['metadata']), open(f'{out}/msk.json', 'w'))
print('done', len(names))
