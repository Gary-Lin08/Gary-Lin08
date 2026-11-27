"""Product-shot render of the Cerebel glasses CAD to transparent PNGs.

Graphite frame with key/fill/rim lighting, clear glass lenses with Fresnel edges, and the
diffractive waveguide (in-coupler, fold/expansion and out-coupler gratings with the faint
rainbow sheen that ambient light produces on surface-relief gratings).

usage: python render_glasses.py glasses.glb outdir [yaw pitch]
"""
import colorsys, json, math, sys
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFilter, ImageChops

src, out = sys.argv[1], sys.argv[2]
YAW = float(sys.argv[3]) if len(sys.argv) > 3 else -48
PITCH = float(sys.argv[4]) if len(sys.argv) > 4 else 20
W, H, SS = 1500, 900, 2
WAVEGUIDE, CLEAR = 'part_0010', 'part_0011'

scene = trimesh.load(src)
Vs, Fs, P, VN = [], [], [], []
off = 0
names = []
for node in scene.graph.nodes_geometry:
    T, g = scene.graph[node]
    m = scene.geometry[g].copy()
    m.apply_transform(T)
    try:
        m = m.smoothed(angle=math.radians(32))
    except Exception:
        pass
    VN.append(m.vertex_normals.copy())
    v = m.vertices
    Vs.append(v); Fs.append(m.faces + off); off += len(v)
    P.append(np.full(len(m.faces), len(names))); names.append(node)
V = np.vstack(Vs); F = np.vstack(Fs); part = np.concatenate(P); VNo = np.vstack(VN)
pid = {n: i for i, n in enumerate(names)}
lens_wg = part == pid[WAVEGUIDE]; lens_cl = part == pid[CLEAR]
is_lens = lens_wg | lens_cl
print('faces', len(F), 'lens faces', is_lens.sum())

# CAD (x across, y back along temples, z up)  ->  world (X=x, Y=z, Z=-y)
def to_world(p):
    p = np.asarray(p, float)
    return np.stack([p[..., 0], p[..., 2], -p[..., 1]], -1)
VW = to_world(V)
center = (VW.max(0) + VW.min(0)) / 2
VW = VW - center

def cam(Pw):
    y, p = math.radians(YAW), math.radians(PITCH)
    x, yy, z = Pw[..., 0], Pw[..., 1], Pw[..., 2]
    x2 = x * math.cos(y) - z * math.sin(y); z2 = x * math.sin(y) + z * math.cos(y)
    y3 = yy * math.cos(p) - z2 * math.sin(p); z3 = yy * math.sin(p) + z2 * math.cos(p)
    return np.stack([x2, y3, z3], -1)

DIST = .42
C = cam(VW)
depth = DIST - C[:, 2]
px, py = C[:, 0] / depth, C[:, 1] / depth
s = min(W * .94 / np.ptp(px), H * .78 / np.ptp(py))
ox = W / 2 - (px.max() + px.min()) / 2 * s; oy = H * .43 + (py.max() + py.min()) / 2 * s

def proj(Pw):
    c = cam(Pw); d = DIST - c[..., 2]
    return np.stack([(ox + c[..., 0] / d * s) * SS, (oy - c[..., 1] / d * s) * SS], -1)

XY = proj(VW)
fn = np.cross(C[F[:, 1]] - C[F[:, 0]], C[F[:, 2]] - C[F[:, 0]])
fn /= np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12
fn_v = fn * np.where(fn[:, 2:3] < 0, -1, 1)          # flip toward camera
vnc = cam(to_world(VNo)); sm = vnc[F].mean(1); sm /= np.linalg.norm(sm, axis=1, keepdims=True) + 1e-12
sm *= np.where((sm * fn).sum(1, keepdims=True) < 0, -1, 1); sm *= np.where(fn[:, 2:3] < 0, -1, 1)
fn_v = np.where(np.isfinite(sm).all(1, keepdims=True), sm, fn_v)
view = np.array([0, 0, 1.0])
key = np.array([-.5, .75, .45]); key /= np.linalg.norm(key)
fill = np.array([.7, .15, .4]); fill /= np.linalg.norm(fill)
rim = np.array([.3, .4, -.85]); rim /= np.linalg.norm(rim)
diff = np.clip(fn_v @ key, 0, 1) * .8 + np.clip(fn_v @ fill, 0, 1) * .25
h = (key + view); h /= np.linalg.norm(h)
spec = np.clip(fn_v @ h, 0, 1) ** 40
fres = (1 - np.abs(fn_v @ view)) ** 3
fdepth = depth[F].mean(1)

adj = m_adj = None
mesh = trimesh.Trimesh(VW, F, process=False)
adj = mesh.face_adjacency
facing = fn[:, 2] > 0
sil = (facing[adj[:, 0]] != facing[adj[:, 1]]) & ~is_lens[adj[:, 0]] & ~is_lens[adj[:, 1]]
sharp = (mesh.face_adjacency_angles > math.radians(70)) & ~is_lens[adj[:, 0]] & ~is_lens[adj[:, 1]]
keep = sil
E = mesh.face_adjacency_edges[keep]; A = adj[keep]
owner = np.where(fdepth[A[:, 0]] < fdepth[A[:, 1]], A[:, 0], A[:, 1])
edges_by_face = {}
for e, o in zip(E, owner):
    edges_by_face.setdefault(int(o), []).append(e)

order = np.argsort(-fdepth)

# ---- waveguide grating regions, defined on the waveguide's front surface (CAD mm)
wgV = V[np.unique(F[lens_wg])]
lo, hi = wgV.min(0), wgV.max(0)
yf = lo[1] - .0002                                    # just in front of the lens surface
def region(pts_mm):
    p = np.array([[x / 1000, yf, z / 1000] for x, z in pts_mm])
    return proj(to_world(p) - center)
cxl = (lo[0] + hi[0]) / 2 * 1000; czl = (lo[2] + hi[2]) / 2 * 1000
outer = lo[0] * 1000                                  # temple-side edge of the waveguide (x most negative)
R_in = [(outer + 6 + 3.2 * math.cos(a), czl + 9 + 3.2 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)]
R_fold = [(outer + 9.5, czl + 11.5), (cxl - 10, czl + 8.5), (cxl - 10, czl + 1.5), (outer + 9.5, czl + 6.5)]
R_out = [(cxl - 13 + 3 * math.cos(a) + (26 if math.cos(a) > 0 else 0) * 0, czl) for a in []] or [(cxl + 11.5 * math.copysign(abs(math.cos(t)) ** .25, math.cos(t)) - 1, czl - 1 + 8.5 * math.copysign(abs(math.sin(t)) ** .25, math.sin(t))) for t in np.linspace(0, 2 * math.pi, 64)]

def hatch(draw, poly, spacing, angle, color, width=1):
    poly = np.asarray(poly)
    mn, mx = poly.min(0), poly.max(0); L = np.linalg.norm(mx - mn)
    c = (mn + mx) / 2; d = np.array([math.cos(angle), math.sin(angle)]); n = np.array([-d[1], d[0]])
    for k in np.arange(-L, L, spacing):
        a = c + n * k - d * L; b = c + n * k + d * L
        draw.line([tuple(a), tuple(b)], fill=color, width=width)

def masked(layer_fn, poly, size):
    mask = Image.new('L', size, 0); ImageDraw.Draw(mask).polygon([tuple(p) for p in poly], fill=255)
    lay = Image.new('RGBA', size, (0, 0, 0, 0)); layer_fn(ImageDraw.Draw(lay), lay)
    a = ImageChops.multiply(lay.getchannel('A'), mask); lay.putalpha(a); return lay

def rainbow(size, poly, alpha):
    poly = np.asarray(poly); mn, mx = poly.min(0), poly.max(0)
    w = max(2, int(mx[0] - mn[0])); hgt = max(2, int(mx[1] - mn[1]))
    g = np.zeros((hgt, w, 4), np.uint8)
    for i in range(w):
        for j in range(0, hgt, max(1, hgt // 60)):
            hue = .72 - .55 * ((i / w) * .7 + (j / hgt) * .3)
            r, gg, bb = colorsys.hsv_to_rgb(hue % 1, .55, 1)
            g[j:j + max(1, hgt // 60), i] = (int(r * 255), int(gg * 255), int(bb * 255), alpha)
    img = Image.new('RGBA', size, (0, 0, 0, 0)); img.paste(Image.fromarray(g, 'RGBA'), (int(mn[0]), int(mn[1])))
    mask = Image.new('L', size, 0); ImageDraw.Draw(mask).polygon([tuple(p) for p in poly], fill=255)
    img.putalpha(ImageChops.multiply(img.getchannel('A'), mask)); return img

THEMES = {
    'light': dict(lo=(34, 38, 44), hi=(132, 140, 152), rimc=(170, 180, 195), line=(10, 12, 16, 90),
                  glass=(205, 220, 235), glass_a=38, edge_a=120, shadow=46, grat=(70, 80, 100, 32)),
    'dark': dict(lo=(40, 45, 53), hi=(150, 160, 175), rimc=(200, 215, 235), line=(220, 230, 245, 60),
                 glass=(70, 95, 125), glass_a=46, edge_a=60, shadow=0, grat=(200, 220, 255, 30)),
}
size = (W * SS, H * SS)
for tname, th in THEMES.items():
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    # contact shadow on an implied floor under the frame
    if th['shadow']:
        floor = VW.copy(); floor[:, 1] = VW[:, 1].min() - .002
        fp = proj(floor[::50])
        hull = trimesh.points.PointCloud(np.c_[fp, np.zeros(len(fp))]).convex_hull
        sh = Image.new('L', size, 0)
        pts2 = hull.vertices[:, :2]
        ang = np.arctan2(pts2[:, 1] - pts2[:, 1].mean(), pts2[:, 0] - pts2[:, 0].mean())
        ImageDraw.Draw(sh).polygon([tuple(p) for p in pts2[np.argsort(ang)]], fill=th['shadow'])
        sh = sh.filter(ImageFilter.GaussianBlur(28 * SS))
        img.paste(Image.new('RGBA', size, (0, 0, 0, 255)), (0, 0), sh)
    dr = ImageDraw.Draw(img)
    lo_c, hi_c, rim_c = np.array(th['lo']), np.array(th['hi']), np.array(th['rimc'])
    lens_mask = Image.new('L', size, 0); lm = ImageDraw.Draw(lens_mask)
    edge_mask = Image.new('L', size, 0); em = ImageDraw.Draw(edge_mask)
    for fi in order:
        a, b, c = F[fi]
        tri = [tuple(XY[a]), tuple(XY[b]), tuple(XY[c])]
        if is_lens[fi]:
            lm.polygon(tri, fill=255)
            em.polygon(tri, fill=int(255 * min(1, fres[fi] * 2.2)))
            continue
        col = lo_c + (hi_c - lo_c) * diff[fi] + (rim_c - lo_c) * fres[fi] * .55
        col = col + (255 - col) * spec[fi] * .7
        col = tuple(int(v) for v in np.clip(col, 0, 255)) + (255,)
        dr.polygon(tri, fill=col, outline=col)
        for e in edges_by_face.get(int(fi), ()):
            dr.line([tuple(XY[e[0]]), tuple(XY[e[1]])], fill=th['line'], width=2)
    # glass: faint tint + Fresnel edges + a soft reflection streak
    glass = Image.new('RGBA', size, th['glass'] + (0,))
    ga = Image.eval(lens_mask, lambda v: v * th['glass_a'] // 255)
    ea = Image.eval(edge_mask, lambda v: v * th['edge_a'] // 255)
    glass.putalpha(ImageChops.lighter(ga, ea))
    streak = Image.new('L', size, 0); sd = ImageDraw.Draw(streak)
    bb = np.array(lens_mask.getbbox())
    for k, (wd, al) in enumerate(((70, 70), (26, 110))):
        x0 = bb[0] + (bb[2] - bb[0]) * (.18 + .5 * k)
        sd.polygon([(x0, bb[1]), (x0 + wd * SS, bb[1]), (x0 + wd * SS - (bb[3] - bb[1]) * .45, bb[3]), (x0 - (bb[3] - bb[1]) * .45, bb[3])], fill=al)
    streak = streak.filter(ImageFilter.GaussianBlur(10 * SS))
    streak = ImageChops.multiply(streak, lens_mask)
    white = Image.new('RGBA', size, (255, 255, 255, 0)); white.putalpha(Image.eval(streak, lambda v: v // 2))
    img = Image.alpha_composite(img, glass)
    img = Image.alpha_composite(img, white)
    # waveguide gratings (clipped to the waveguide's visible silhouette)
    wg_mask = Image.new('L', size, 0); wd_ = ImageDraw.Draw(wg_mask)
    for fi in np.where(lens_wg)[0]:
        a, b, c = F[fi]; wd_.polygon([tuple(XY[a]), tuple(XY[b]), tuple(XY[c])], fill=255)
    pin, pfold, pout = region(R_in), region(R_fold), region(R_out)
    layers = [rainbow(size, pout, 24), rainbow(size, pfold, 12), rainbow(size, pin, 48)]
    hat = Image.new('RGBA', size, (0, 0, 0, 0))
    hat = Image.alpha_composite(hat, masked(lambda d, l: hatch(d, pout, 3.2 * SS, math.radians(84), th['grat'], 1), pout, size))
    hat = Image.alpha_composite(hat, masked(lambda d, l: hatch(d, pfold, 3.2 * SS, math.radians(40), th['grat'], 1), pfold, size))
    hat = Image.alpha_composite(hat, masked(lambda d, l: hatch(d, pin, 2.2 * SS, math.radians(84), th['grat'], 1), pin, size))
    glow = Image.new('RGBA', size, (92, 255, 138, 0)); gm = Image.new('L', size, 0)
    ImageDraw.Draw(gm).polygon([tuple(p) for p in pout], fill=26); gm = gm.filter(ImageFilter.GaussianBlur(6 * SS)); glow.putalpha(gm)
    outline = Image.new('RGBA', size, (0, 0, 0, 0)); od = ImageDraw.Draw(outline)
    for poly in (pin, pout):
        od.line([tuple(p) for p in np.vstack([poly, poly[:1]])], fill=th['grat'][:3] + (40,), width=1)
    for lay in layers + [hat, glow, outline]:
        lay.putalpha(ImageChops.multiply(lay.getchannel('A').filter(ImageFilter.GaussianBlur(1.2 * SS)), wg_mask))
        img = Image.alpha_composite(img, lay)
    img = img.resize((W, H), Image.LANCZOS)
    img.save(f'{out}/glasses-cad-{tname}.png', optimize=True)
    print('saved', tname)

# anchors for callouts, in output pixels
def anchor(p_mm):
    q = proj(to_world(np.array(p_mm) / 1000) - center) / SS
    return [round(float(q[0]), 1), round(float(q[1]), 1)]
ctr = lambda n: (lambda v: ((v.min(0) + v.max(0)) / 2 * 1000).tolist())(V[np.unique(F[part == pid[n]])])
anchors = dict(incoupler=anchor([R_in[0][0] - 3.2, yf * 1000, R_in[0][1]]),
               outcoupler=anchor([cxl, yf * 1000, czl - 1]),
               fold=anchor([(outer + cxl) / 2, yf * 1000, czl + 8]),
               engine=anchor(ctr('part_0008')), clear=anchor(ctr(CLEAR)),
               temple_l=anchor(ctr('part_0015')), temple_r=anchor(ctr('part_0020')),
               top=anchor(ctr('part_0598')))
json.dump(dict(W=W, H=H, anchors=anchors), open(f'{out}/glasses-anchors.json', 'w'), indent=1)
print(anchors)
