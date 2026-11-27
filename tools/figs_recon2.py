"""Figure 3: one real session, three views. Exec'd last; overrides reconstruct()."""
import base64, glob, json, os

_HERE_R = os.path.dirname(os.path.abspath(__file__))


def reconstruct():
    M = json.load(open(os.path.join(_HERE_R, 'motion.json')))
    Jt = M['joints']; E = M['edges']; fps = M['fps']
    T_ = len(Jt); DUR = T_ / fps
    W, H = 1200, 520
    b = f'<text x="0" y="22" class="caps">A · GEM-X, 77 JOINTS</text><line x1="0" y1="34" x2="360" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="390" y="22" class="caps">B · OPENSIM, RAJAGOPAL MODEL</text><line x1="390" y1="34" x2="760" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="790" y="22" class="caps">C · JOINT ANGLES FROM IK</text><line x1="790" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    xs = [p[0] for fr in Jt for p in fr]; zs = [p[2] for fr in Jt for p in fr]
    cx0, cz0 = (max(xs) + min(xs)) / 2, (max(zs) + min(zs)) / 2
    cam = Cam(yaw=-35, pitch=8, dist=4.0, F=620, cx=180, cy=262, target=(0, .95, 0))
    P = lambda p: cam.p((p[0] - cx0, p[1], p[2] - cz0))
    for i in range(-4, 5):
        a, c = P((cx0 + i * .25, 0, cz0 - 1)), P((cx0 + i * .25, 0, cz0 + 1))
        b += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(c[0])}" y2="{f(c[1])}" stroke="{T["hair"]}" stroke-width=".6"/>'
        a, c = P((cx0 - 1, 0, cz0 + i * .25)), P((cx0 + 1, 0, cz0 + i * .25))
        b += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(c[0])}" y2="{f(c[1])}" stroke="{T["hair"]}" stroke-width=".6"/>'
    for fr in range(0, T_, 15):
        pts = [P(p) for p in Jt[fr]]
        d = ''.join(f'M{f(pts[a][0])} {f(pts[a][1])} L{f(pts[c][0])} {f(pts[c][1])}' for a, c in E)
        b += f'<path d="{d}" fill="none" stroke="{T["ink"]}" stroke-opacity=".08" stroke-width="1.2" stroke-linecap="round"/>'
    for j in M['trail'][:2]:
        tr = [P(Jt[fr][j]) for fr in range(T_)]
        b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in tr)}" fill="none" stroke="{T["acc"]}" stroke-opacity=".45" stroke-width="1" stroke-dasharray="1.5 3"/>'
    frames = list(range(T_)) + [0]
    def dpath(fr):
        pts = [P(p) for p in Jt[fr]]
        return ''.join(f'M{f(pts[a][0])} {f(pts[a][1])} L{f(pts[c][0])} {f(pts[c][1])}' for a, c in E)
    ds = [dpath(fr) for fr in frames]
    b += f'<path d="{ds[0]}" fill="none" stroke="{T["acc"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="d" values="{";".join(ds)}" dur="{f(DUR)}s" repeatCount="indefinite"/></path>'
    dd = [''.join(f'M{f(x-1.5)} {f(y)} a1.5 1.5 0 1 0 3 0 a1.5 1.5 0 1 0 -3 0' for x, y in (P(p) for p in Jt[fr])) for fr in frames]
    b += f'<path d="{dd[0]}" fill="{T["ink2"]}"><animate attributeName="d" values="{";".join(dd)}" dur="{f(DUR)}s" repeatCount="indefinite"/></path>'
    # B: real OpenSim render, frame stack
    files = sorted(glob.glob(os.path.join(_HERE_R, 'msk', f'msk-{TN}-*.webp')))
    n = len(files)
    iw, ih = 300, 442; ix, iy = 425, 44
    for i, fp in enumerate(files):
        data = base64.b64encode(open(fp, 'rb').read()).decode()
        t0 = i / n; t1 = (i + 1) / n
        if i == 0:
            vals, kt = '1;0;0', f'0;{t1:.5f};1'
        else:
            vals, kt = ('0;1;0', f'0;{t0:.5f};1') if i == n - 1 else ('0;1;0;0', f'0;{t0:.5f};{t1:.5f};1')
        b += (f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="data:image/webp;base64,{data}" opacity="{1 if i == 0 else 0}">'
              f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{f(DUR)}s" repeatCount="indefinite"/></image>')
    b += f'<text x="390" y="500" class="mono mute" font-size="12">24 bodies · 80 muscle paths · {n} frames</text>'
    # C: IK small multiples
    names = {'lumbar_bending': 'trunk side-bend', 'neck_rotation': 'neck rotation', 'elbow_flex_r': 'right elbow flexion', 'arm_flex_l': 'left shoulder flexion'}
    t = M['ik_time']; tmax = t[-1]
    x0, x1 = 930, 1195
    rh, top = 104, 56
    for r, (key, vals) in enumerate(M['ik'].items()):
        y0 = top + r * rh; y1 = y0 + rh - 36
        lo, hi = min(vals), max(vals); pad = (hi - lo) * .1 + 1; lo -= pad; hi += pad
        X = lambda tt: x0 + (x1 - x0) * tt / tmax
        Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
        b += f'<text x="790" y="{y0+22}" class="serif" font-size="15" font-style="italic">{names[key]}</text>'
        b += f'<text x="790" y="{y0+42}" class="mono mute" font-size="12">{min(vals):.0f}° … {max(vals):.0f}°</text>'
        b += f'<line x1="{x0}" y1="{f(y1)}" x2="{x1}" y2="{f(y1)}" stroke="{T["hair"]}" stroke-width=".6"/>'
        d = 'M' + ' L'.join(f'{f(X(tt))} {f(Y(v))}' for tt, v in zip(t, vals))
        col = T['acc'] if r == 0 else T['ink']
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>'
        cxs = ';'.join(f(X(tt)) for tt in t) + f';{f(X(t[0]))}'; cys = ';'.join(f(Y(v)) for v in vals) + f';{f(Y(vals[0]))}'
        b += (f'<circle r="3.4" fill="{col}" cx="{f(X(t[0]))}" cy="{f(Y(vals[0]))}"><animate attributeName="cx" values="{cxs}" dur="{f(DUR)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{cys}" dur="{f(DUR)}s" repeatCount="indefinite"/></circle>')
    b += (f'<line x1="{x0}" y1="{top}" x2="{x0}" y2="{top+4*rh-36}" stroke="{T["ink"]}" stroke-opacity=".4" stroke-width=".8">'
          f'<animate attributeName="x1" values="{x0};{x1}" dur="{f(DUR)}s" repeatCount="indefinite"/><animate attributeName="x2" values="{x0};{x1}" dur="{f(DUR)}s" repeatCount="indefinite"/></line>')
    b += f'<text x="{x0}" y="{top+4*rh-16}" class="mono mute" font-size="12">0 s</text><text x="{x1}" y="{top+4*rh-16}" class="mono mute" font-size="12" text-anchor="end">{tmax:.0f} s</text>'
    b += f'<text x="0" y="500" class="mono mute" font-size="12">30 fps · {T_} frames · same session in A, B and C</text>'
    save(f'recon-{TN}.svg', svg(W, H, b))
