"""Figures built from real assets: the glasses CAD render and one real motion session.
Exec'd after figs_body.py; overrides glasses() and reconstruct()."""
import base64, json, math, os

_HERE = os.path.dirname(os.path.abspath(__file__))


def glasses():
    W, H = 1200, 640
    png = os.path.join(_HERE, f'glasses-cad-{TN}.png')
    AN = json.load(open(os.path.join(_HERE, 'glasses-anchors.json')))['anchors']
    data = base64.b64encode(open(png, 'rb').read()).decode()
    iw, ih, ix, iy = 840, 504, 0, 36
    k = iw / 1500
    b = f'<text x="0" y="22" class="caps">A · CEREBEL GLASSES, FROM THE PRODUCTION CAD</text><line x1="0" y1="34" x2="840" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="880" y="22" class="caps">B · WHAT THE WEARER SEES</text><line x1="880" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    b += f'<image x="{ix}" y="{iy}" width="{iw}" height="{ih}" href="data:image/png;base64,{data}"/>'
    A = lambda px, py: (ix + px * k, iy + py * k)
    callouts = [
        (tuple(AN['temple_l']), 'Temple electronics', 'SoC, Wi-Fi / BT, battery'),
        ((AN['engine'][0] + 30, AN['engine'][1] + 12), 'Camera', '1080p photo and video'),
        (tuple(AN['incoupler']), 'In-coupler grating', 'microLED light enters the glass'),
        (tuple(AN['outcoupler']), 'Out-coupler, eyebox', 'faint rainbow is ambient light'),
        (tuple(AN['clear']), 'Clear lens', 'no display on this side'),
        (tuple(AN['top']), 'Electronics module', 'housed above the clear lens'),
    ]
    for i, ((px, py), t1, t2) in enumerate(callouts):
        ax, ay = A(px, py)
        b += (f'<circle cx="{f(ax)}" cy="{f(ay)}" r="11" fill="none" stroke="{T["acc"]}" stroke-width="1.2">'
              f'<animate attributeName="r" values="11;17;11" dur="3s" begin="{f(i*.5)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="stroke-opacity" values=".9;0;.9" dur="3s" begin="{f(i*.5)}s" repeatCount="indefinite"/></circle>')
        b += f'<circle cx="{f(ax)}" cy="{f(ay)}" r="10" fill="{T["acc"]}"/>'
        b += f'<text x="{f(ax)}" y="{f(ay+4.5)}" font-size="12.5" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>'
        col, row = i % 3, i // 3
        lx, ly = col * 285, iy + ih + 22 + row * 44
        b += f'<circle cx="{lx+9}" cy="{ly-5}" r="9" fill="none" stroke="{T["acc"]}"/><text x="{lx+9}" y="{ly-1}" font-size="11.5" font-weight="700" fill="{T["acc"]}" text-anchor="middle">{i+1}</text>'
        b += f'<text x="{lx+26}" y="{ly}" font-size="14.5" font-weight="600">{t1}</text>'
        b += f'<text x="{lx+26}" y="{ly+17}" class="mono mute" font-size="12">{t2}</text>'
    # (B) the display
    dx, dy, dw, dh = 880, 64, 320, 240
    g = '#5CFF8A'
    b += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="10" fill="#050806" stroke="{T["hair"]}"/>'
    b += f'<text x="{dx+16}" y="{dy+28}" class="mono" font-size="13" fill="{g}" fill-opacity=".7">10:42</text>'
    b += f'<text x="{dx+dw-16}" y="{dy+28}" class="mono" font-size="13" fill="{g}" fill-opacity=".7" text-anchor="end">REC ●</text>'
    lines = [('“Hey Cerebel,', .05), ('how was that swing?”', .14), ('Lead knee 162°', .36), ('at impact.', .42), ('Stay flexed next rep.', .52)]
    for i, (txt, t) in enumerate(lines):
        big = i >= 2
        y = dy + 66 + i * 30 + (12 if big else 0)
        b += (f'<text x="{dx+20}" y="{y}" class="mono" font-size="{20 if big else 15}" fill="{g}" fill-opacity="{1 if big else .65}" opacity="0">{txt}'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t};{f(t+.02)};.92;1" dur="9s" repeatCount="indefinite"/></text>')
    for kk in range(9):
        h = 6 + 10 * abs(math.sin(kk * 1.3))
        b += (f'<rect x="{dx+dw-110+kk*10}" y="{f(dy+dh-24-h/2)}" width="5" height="{f(h)}" rx="2" fill="{g}" fill-opacity=".7">'
              f'<animate attributeName="height" values="{f(h)};{f(h*.3)};{f(h)}" dur="{f(.7+kk%4*.15)}s" repeatCount="indefinite"/></rect>')
    b += f'<text x="{dx+20}" y="{dy+dh-18}" class="mono" font-size="12" fill="{g}" fill-opacity=".55">listening</text>'
    b += f'<text x="{dx}" y="{dy+dh+26}" class="serif mute" font-size="14" font-style="italic">640 × 480, green microLED;</text>'
    b += f'<text x="{dx}" y="{dy+dh+46}" class="serif mute" font-size="14" font-style="italic">black is transparent on the lens.</text>'
    # light path schematic
    ly0 = dy + dh + 92
    b += f'<text x="{dx}" y="{ly0-26}" class="caps">C · LIGHT PATH IN THE WAVEGUIDE</text><line x1="{dx}" y1="{ly0-14}" x2="1200" y2="{ly0-14}" stroke="{T["hair"]}"/>'
    steps = [('microLED', 0), ('in', 78), ('fold', 150), ('out', 222), ('eye', 296)]
    for i, (lab, x) in enumerate(steps):
        X0 = dx + x
        if lab == 'microLED':
            b += f'<rect x="{X0}" y="{ly0+6}" width="26" height="18" rx="3" fill="none" stroke="{g}" stroke-opacity=".9"/>'
        elif lab == 'eye':
            b += f'<path d="M{X0} {ly0+15} q12 -11 24 0 q-12 11 -24 0z" fill="none" stroke="{T["ink"]}"/><circle cx="{X0+12}" cy="{ly0+15}" r="3.5" fill="{T["ink"]}"/>'
        else:
            b += f'<rect x="{X0}" y="{ly0+4}" width="26" height="22" rx="3" fill="{T["faint"]}" stroke="{T["hair"]}"/>'
            for k2 in range(5):
                b += f'<line x1="{X0+4+k2*4.5}" y1="{ly0+7}" x2="{X0+4+k2*4.5}" y2="{ly0+23}" stroke="{T["mute"]}" stroke-width=".7"/>'
        b += f'<text x="{X0+13}" y="{ly0+44}" class="mono mute" font-size="11.5" text-anchor="middle">{lab}</text>'
    b += f'<line x1="{dx}" y1="{ly0+15}" x2="{dx+296}" y2="{ly0+15}" stroke="{T["hair"]}" stroke-dasharray="2 3"/>'
    zig = f'M{dx+26} {ly0+15} L{dx+91} {ly0+15} L{dx+110} {ly0+4} L{dx+130} {ly0+26} L{dx+150} {ly0+4} L{dx+170} {ly0+26} L{dx+190} {ly0+4} L{dx+210} {ly0+26} L{dx+235} {ly0+15} L{dx+296} {ly0+15}'
    b += f'<path id="lp" d="{zig}" fill="none" stroke="{g}" stroke-opacity=".35" stroke-width="1"/>'
    b += f'<circle r="3.2" fill="{g}"><animateMotion dur="2.6s" repeatCount="indefinite"><mpath xlink:href="#lp"/></animateMotion></circle>'
    b += f'<text x="{dx}" y="{ly0+72}" class="serif mute" font-size="13.5" font-style="italic">Total internal reflection between gratings; schematic.</text>'
    save(f'glasses-{TN}.svg', svg(W, H, b))


def reconstruct():
    M = json.load(open(os.path.join(_HERE, 'motion.json')))
    Jt = M['joints']; E = M['edges']; fps = M['fps']
    T_ = len(Jt); DUR = T_ / fps
    W, H = 1200, 500
    b = f'<text x="0" y="22" class="caps">A · GEM-X, 77 BODY JOINTS FROM ONE PHONE VIDEO</text><line x1="0" y1="34" x2="560" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="610" y="22" class="caps">B · OPENSIM INVERSE KINEMATICS, SAME SESSION</text><line x1="610" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    # centre the motion
    xs = [p[0] for fr in Jt for p in fr]; zs = [p[2] for fr in Jt for p in fr]
    cx0, cz0 = (max(xs) + min(xs)) / 2, (max(zs) + min(zs)) / 2
    cam = Cam(yaw=-28, pitch=10, dist=4.6, F=740, cx=280, cy=250, target=(0, .95, 0))
    P = lambda p: cam.p((p[0] - cx0, p[1], p[2] - cz0))
    # floor grid
    for i in range(-4, 5):
        a, c = P((cx0 + i * .2, 0, cz0 - .8)), P((cx0 + i * .2, 0, cz0 + .8))
        b += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(c[0])}" y2="{f(c[1])}" stroke="{T["hair"]}" stroke-width=".6"/>'
        a, c = P((cx0 - .8, 0, cz0 + i * .2)), P((cx0 + .8, 0, cz0 + i * .2))
        b += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(c[0])}" y2="{f(c[1])}" stroke="{T["hair"]}" stroke-width=".6"/>'
    # stroboscopic ghosts
    for fr in range(0, T_, 15):
        pts = [P(p) for p in Jt[fr]]
        d = ''.join(f'M{f(pts[a][0])} {f(pts[a][1])} L{f(pts[c][0])} {f(pts[c][1])}' for a, c in E)
        b += f'<path d="{d}" fill="none" stroke="{T["ink"]}" stroke-opacity=".09" stroke-width="1.2" stroke-linecap="round"/>'
    # trails of the most-moving extremities (real paths)
    for j in M['trail'][:2]:
        tr = [P(Jt[fr][j]) for fr in range(T_)]
        b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in tr)}" fill="none" stroke="{T["acc"]}" stroke-opacity=".45" stroke-width="1" stroke-dasharray="1.5 3"/>'
    # floor shadow + animated skeleton (every frame)
    step = 1
    frames = list(range(0, T_, step)) + [0]
    def dpath(fr, shadow=False):
        pts = [P((p[0], 0.0, p[2])) if shadow else P(p) for p in Jt[fr]]
        return ''.join(f'M{f(pts[a][0])} {f(pts[c][1] if False else pts[a][1])} L{f(pts[c][0])} {f(pts[c][1])}' for a, c in E)
    sh = [dpath(fr, True) for fr in frames]
    b += f'<path d="{sh[0]}" fill="none" stroke="{T["ink"]}" stroke-opacity=".08" stroke-width="3" stroke-linecap="round"><animate attributeName="d" values="{";".join(sh)}" dur="{f(DUR)}s" repeatCount="indefinite"/></path>'
    ds = [dpath(fr) for fr in frames]
    b += f'<path d="{ds[0]}" fill="none" stroke="{T["acc"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="d" values="{";".join(ds)}" dur="{f(DUR)}s" repeatCount="indefinite"/></path>'
    def dots(fr):
        return ''.join(f'M{f(x-1.6)} {f(y)} a1.6 1.6 0 1 0 3.2 0 a1.6 1.6 0 1 0 -3.2 0' for x, y in (P(p) for p in Jt[fr]))
    dd = [dots(fr) for fr in frames]
    b += f'<path d="{dd[0]}" fill="{T["ink2"]}"><animate attributeName="d" values="{";".join(dd)}" dur="{f(DUR)}s" repeatCount="indefinite"/></path>'
    for k in range(10):
        b += (f'<text x="0" y="470" class="mono mute" font-size="12" opacity="{1 if k == 0 else 0}">t = {k*DUR/10:.1f} s · 30 fps · 151 frames'
              f'<animate attributeName="opacity" values="{";".join("1" if j == k else "0" for j in range(10))}" calcMode="discrete" dur="{f(DUR)}s" repeatCount="indefinite"/></text>')
    # (B) small multiples of real IK angles
    names = {'lumbar_bending': 'trunk side-bend', 'neck_rotation': 'neck rotation', 'elbow_flex_r': 'right elbow flexion', 'arm_flex_l': 'left shoulder flexion'}
    t = M['ik_time']; tmax = t[-1]
    x0, x1 = 760, 1190
    rows = list(M['ik'].items())
    rh, top = 96, 60
    for r, (key, vals) in enumerate(rows):
        y0 = top + r * rh; y1 = y0 + rh - 34
        lo, hi = min(vals), max(vals); pad = (hi - lo) * .1 + 1; lo -= pad; hi += pad
        X = lambda tt: x0 + (x1 - x0) * tt / tmax
        Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
        b += f'<text x="610" y="{y0+20}" class="serif" font-size="15" font-style="italic">{names[key]}</text>'
        b += f'<text x="610" y="{y0+40}" class="mono mute" font-size="12">{min(vals):.0f}° … {max(vals):.0f}°</text>'
        b += f'<line x1="{x0}" y1="{f(y1)}" x2="{x1}" y2="{f(y1)}" stroke="{T["hair"]}" stroke-width=".6"/>'
        d = 'M' + ' L'.join(f'{f(X(tt))} {f(Y(v))}' for tt, v in zip(t, vals))
        col = T['acc'] if r == 0 else T['ink']
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>'
        cxs = ';'.join(f(X(tt)) for tt in t) + f';{f(X(t[0]))}'; cys = ';'.join(f(Y(v)) for v in vals) + f';{f(Y(vals[0]))}'
        b += (f'<circle r="3.4" fill="{col}" cx="{f(X(t[0]))}" cy="{f(Y(vals[0]))}"><animate attributeName="cx" values="{cxs}" dur="{f(DUR)}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{cys}" dur="{f(DUR)}s" repeatCount="indefinite"/></circle>')
    b += (f'<line x1="{x0}" y1="{top}" x2="{x0}" y2="{top+4*rh-34}" stroke="{T["ink"]}" stroke-opacity=".4" stroke-width=".8">'
          f'<animate attributeName="x1" values="{x0};{x1}" dur="{f(DUR)}s" repeatCount="indefinite"/><animate attributeName="x2" values="{x0};{x1}" dur="{f(DUR)}s" repeatCount="indefinite"/></line>')
    b += f'<text x="{x0}" y="{top+4*rh-14}" class="mono mute" font-size="12">0 s</text><text x="{x1}" y="{top+4*rh-14}" class="mono mute" font-size="12" text-anchor="end">{tmax:.0f} s</text>'
    save(f'recon-{TN}.svg', svg(W, H, b))
