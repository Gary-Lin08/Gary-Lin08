"""Reconstruction turntable and AR-glasses line drawing. Exec'd after figs3d.py inside gen2.py."""
import math

# ------------------------------------------------------------------ video -> mesh -> musculoskeletal
BODY = dict(P=(0, .95, 0), S=(0, 1.42, .02), Hc=(0, 1.64, .03), N=(0, 1.5, .02),
            Ls=(.19, 1.41, .02), Rs=(-.19, 1.41, .02), Le=(.27, 1.15, .07), Re=(-.25, 1.14, .1), Lw=(.27, .92, .17), Rw=(-.22, .93, .24),
            Lh=(.1, .93, 0), Rh=(-.1, .93, 0), Lk=(.13, .52, .08), Rk=(-.12, .52, .06), La=(.15, .08, 0), Ra=(-.14, .08, -.02))
SEGS = [
    ('P', 'S', [(.15, .1), (.14, .095), (.13, .09), (.15, .1), (.17, .11)]),
    ('Ls', 'Le', [(.048, .048), (.04, .04)]), ('Rs', 'Re', [(.048, .048), (.04, .04)]),
    ('Le', 'Lw', [(.038, .038), (.027, .027)]), ('Re', 'Rw', [(.038, .038), (.027, .027)]),
    ('Lh', 'Lk', [(.082, .082), (.065, .065), (.05, .05)]), ('Rh', 'Rk', [(.082, .082), (.065, .065), (.05, .05)]),
    ('Lk', 'La', [(.052, .052), (.05, .05), (.034, .034)]), ('Rk', 'Ra', [(.052, .052), (.05, .05), (.034, .034)]),
    ('S', 'N', [(.06, .055), (.05, .05)]),
]


def _basis(d):
    ref = (0, 0, 1) if abs(d[2]) < .9 else (1, 0, 0)
    e1 = v_unit(v_cross(d, ref)); e2 = v_cross(d, e1)
    return e1, e2


def mesh_paths(rings=6, pts=11, merid=8):
    out = []
    for a, b, prof in SEGS:
        A, B = BODY[a], BODY[b]; d = v_unit(v_sub(B, A)); e1, e2 = _basis(d)
        L = v_len(v_sub(B, A))
        def R(t, prof=prof):
            k = t * (len(prof) - 1); i = min(int(k), len(prof) - 2); u = k - i
            return (prof[i][0] + (prof[i + 1][0] - prof[i][0]) * u, prof[i][1] + (prof[i + 1][1] - prof[i][1]) * u)
        def pt(t, ang, A=A, d=d, L=L, e1=e1, e2=e2, R=R):
            rx, rz = R(t); c = v_add(A, v_mul(d, L * t))
            return v_add(c, v_add(v_mul(e1, rx * math.cos(ang)), v_mul(e2, rz * math.sin(ang))))
        for r in range(rings):
            t = r / (rings - 1)
            out.append([pt(t, 2 * math.pi * k / (pts - 1)) for k in range(pts)])
        for m in range(merid):
            ang = 2 * math.pi * m / merid
            out.append([pt(r / (rings - 1), ang) for r in range(rings)])
    Hc, rh = BODY['Hc'], .1
    for k in range(5):
        y = -.8 + .4 * k; rr = rh * math.sqrt(1 - y * y)
        out.append([(Hc[0] + rr * math.cos(2 * math.pi * j / 12), Hc[1] + rh * y * 1.15, Hc[2] + rr * .9 * math.sin(2 * math.pi * j / 12)) for j in range(13)])
    for m in range(6):
        ang = math.pi * m / 6
        out.append([(Hc[0] + rh * math.sin(math.pi * j / 10) * math.cos(ang), Hc[1] + rh * 1.15 * math.cos(math.pi * j / 10),
                     Hc[2] + rh * .9 * math.sin(math.pi * j / 10) * math.sin(ang)) for j in range(11)])
    return out


MUSCLES = [
    (('Lh', (.02, .02, .07)), ('Lk', (0, .05, .05)), (0, 0, .05)), (('Rh', (-.02, .02, .07)), ('Rk', (0, .05, .05)), (0, 0, .05)),
    (('Lh', (0, -.02, -.06)), ('Lk', (0, .04, -.04)), (0, 0, -.05)), (('Rh', (0, -.02, -.06)), ('Rk', (0, .04, -.04)), (0, 0, -.05)),
    (('Lk', (0, -.02, -.04)), ('La', (0, .04, -.05)), (0, 0, -.04)), (('Rk', (0, -.02, -.04)), ('Ra', (0, .04, -.05)), (0, 0, -.04)),
    (('P', (.08, .02, -.08)), ('Lh', (.05, -.1, -.05)), (.03, 0, -.05)), (('P', (-.08, .02, -.08)), ('Rh', (-.05, -.1, -.05)), (-.03, 0, -.05)),
    (('P', (.04, .05, -.08)), ('S', (.05, -.05, -.07)), (0, 0, -.03)), (('P', (-.04, .05, -.08)), ('S', (-.05, -.05, -.07)), (0, 0, -.03)),
    (('P', (.1, .08, .05)), ('S', (.12, -.18, .07)), (.03, 0, .03)), (('P', (-.1, .08, .05)), ('S', (-.12, -.18, .07)), (-.03, 0, .03)),
    (('Ls', (0, .03, .03)), ('Le', (0, .05, .04)), (0, 0, .035)), (('Rs', (0, .03, .03)), ('Re', (0, .05, .04)), (0, 0, .035)),
    (('Ls', (.02, 0, -.03)), ('Le', (0, .03, -.04)), (.01, 0, -.03)), (('Rs', (-.02, 0, -.03)), ('Re', (0, .03, -.04)), (-.01, 0, -.03)),
    (('S', (.05, .06, 0)), ('Ls', (.03, -.06, 0)), (0, .04, 0)), (('S', (-.05, .06, 0)), ('Rs', (-.03, -.06, 0)), (0, .04, 0)),
]


def msk_paths():
    bones = [('P', 'S'), ('Ls', 'Le'), ('Le', 'Lw'), ('Rs', 'Re'), ('Re', 'Rw'), ('Lh', 'Lk'), ('Lk', 'La'), ('Rh', 'Rk'), ('Rk', 'Ra'), ('S', 'N'), ('Ls', 'Rs'), ('Lh', 'Rh')]
    Bn = [[BODY[a], BODY[b]] for a, b in bones]
    rings = []
    S = BODY['S']
    for k in range(6):
        y = S[1] - .04 - k * .05; rx = .13 - .007 * k; rz = .09 - .004 * k
        rings.append([(rx * math.cos(2 * math.pi * j / 16), y - .02 * abs(math.sin(2 * math.pi * j / 16)), S[2] + rz * math.sin(2 * math.pi * j / 16)) for j in range(17)])
    P = BODY['P']
    rings.append([(.14 * math.cos(2 * math.pi * j / 16), P[1] + .03 * math.sin(2 * math.pi * j / 16) ** 2, P[2] + .09 * math.sin(2 * math.pi * j / 16)) for j in range(17)])
    Hc, rh = BODY['Hc'], .09
    rings += [[(Hc[0] + rh * math.cos(2 * math.pi * j / 16), Hc[1] + rh * 1.2 * math.sin(2 * math.pi * j / 16), Hc[2]) for j in range(17)],
              [(Hc[0], Hc[1] + rh * 1.2 * math.sin(2 * math.pi * j / 16), Hc[2] + rh * math.cos(2 * math.pi * j / 16)) for j in range(17)]]
    mus = []
    for (ja, oa), (jb, ob), bulge in MUSCLES:
        A = v_add(BODY[ja], oa); Bp = v_add(BODY[jb], ob); M = v_add(v_mul(v_add(A, Bp), .5), bulge)
        mus.append([v_add(v_add(v_mul(A, (1 - t) ** 2), v_mul(M, 2 * t * (1 - t))), v_mul(Bp, t * t)) for t in [k / 10 for k in range(11)]])
    return Bn, rings, mus


def turntable_d(polys, cam, frames, origin):
    ds = []
    for fr in range(frames):
        ang = 2 * math.pi * fr / frames
        parts = []
        for poly in polys:
            q = [cam.p(v_add(rot(v_sub(p, origin), (0, 1, 0), ang), origin)) for p in poly]
            parts.append('M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in q))
        ds.append(''.join(parts))
    return ds


def reconstruct():
    W, H = 1200, 500
    FR, DUR = 30, 14
    b = ''
    for x, t in ((0, 'A · INPUT FRAME, MONOCULAR VIDEO'), (410, 'B · BODY MESH'), (810, 'C · MUSCULOSKELETAL MODEL')):
        b += f'<text x="{x}" y="22" class="caps">{t}</text><line x1="{x}" y1="34" x2="{x+370}" y2="34" stroke="{T["hair"]}"/>'
    for x, lab in ((340, 'GEM-X'), (740, 'OpenSim IK')):
        b += f'<path d="M{x} 250 L{x+56} 250" stroke="{T["mute"]}" stroke-width="1.1" marker-end="url(#arr)"/>'
        b += f'<text x="{x+28}" y="238" class="serif" font-size="14" font-style="italic" fill="{T["acc"]}" text-anchor="middle">{lab}</text>'
    fx, fy, fw, fh = 0, 70, 320, 360
    b += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{T["faint"]}" stroke="{T["hair"]}"/>'
    cam2 = Cam(yaw=-20, pitch=4, dist=4.2, F=420, cx=fx + fw / 2, cy=fy + fh / 2 + 10, target=(0, .85, 0))
    sil = [('P', 'S'), ('S', 'N'), ('Ls', 'Le'), ('Le', 'Lw'), ('Rs', 'Re'), ('Re', 'Rw'), ('Lh', 'Lk'), ('Lk', 'La'), ('Rh', 'Rk'), ('Rk', 'Ra'), ('Ls', 'Rs'), ('Lh', 'Rh')]
    for a, z in sil:
        p, q = cam2.p(BODY[a]), cam2.p(BODY[z])
        w = 34 if (a, z) == ('P', 'S') else (22 if a in ('Lh', 'Rh') else 15)
        b += f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="{T["mute"]}" stroke-opacity=".25" stroke-width="{w}" stroke-linecap="round"/>'
    hc = cam2.p(BODY['Hc']); b += f'<circle cx="{f(hc[0])}" cy="{f(hc[1])}" r="15" fill="{T["mute"]}" fill-opacity=".25"/>'
    for a, z in sil:
        p, q = cam2.p(BODY[a]), cam2.p(BODY[z])
        b += f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="{T["acc2"]}" stroke-width="1.4"/>'
    for i, k in enumerate(('Hc', 'N', 'Ls', 'Rs', 'Le', 'Re', 'Lw', 'Rw', 'Lh', 'Rh', 'Lk', 'Rk', 'La', 'Ra')):
        p = cam2.p(BODY[k])
        b += f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="3.2" fill="{T["acc2"]}"><animate attributeName="r" values="3.2;4.4;3.2" dur="2.4s" begin="{f(i*.12)}s" repeatCount="indefinite"/></circle>'
    b += f'<rect x="{fx+84}" y="{fy+44}" width="{fw-168}" height="{fh-70}" fill="none" stroke="{T["acc2"]}" stroke-dasharray="4 3" stroke-width="1"/>'
    b += f'<text x="{fx+86}" y="{fy+38}" class="mono" font-size="12" fill="{T["acc2"]}">person 0.98</text>'
    for k in range(10):
        b += (f'<text x="{fx+10}" y="{fy+fh-12}" class="mono mute" font-size="12" opacity="{1 if k == 0 else 0}">frame {142+k:04d}'
              f'<animate attributeName="opacity" values="{";".join("1" if j == k else "0" for j in range(10))}" calcMode="discrete" dur="2.5s" repeatCount="indefinite"/></text>')
    origin = (0, .9, 0)
    camB = Cam(yaw=0, pitch=6, dist=4.0, F=820, cx=590, cy=255, target=(0, .85, 0))
    camC = Cam(yaw=0, pitch=6, dist=4.0, F=820, cx=990, cy=255, target=(0, .85, 0))
    for cam_ in (camB, camC):
        g1, g2 = cam_.p((-.45, 0, 0)), cam_.p((.45, 0, 0))
        b += f'<ellipse cx="{f((g1[0]+g2[0])/2)}" cy="{f(g1[1])}" rx="{f((g2[0]-g1[0])/2)}" ry="16" fill="none" stroke="{T["hair"]}"/>'
    ds = turntable_d(mesh_paths(), camB, FR, origin)
    b += f'<path d="{ds[0]}" fill="none" stroke="{T["ink"]}" stroke-opacity=".55" stroke-width=".7" stroke-linejoin="round"><animate attributeName="d" values="{";".join(ds + [ds[0]])}" dur="{DUR}s" repeatCount="indefinite"/></path>'
    bones, rings, mus = msk_paths()
    for polys, col, wd, op in ((rings, T['ink'], .9, .55), (bones, T['ink'], 2.6, .9), (mus, T['acc'], 3.2, .55)):
        ds = turntable_d(polys, camC, FR, origin)
        b += f'<path d="{ds[0]}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{wd}" stroke-linecap="round" stroke-linejoin="round"><animate attributeName="d" values="{";".join(ds + [ds[0]])}" dur="{DUR}s" repeatCount="indefinite"/></path>'
    jd = turntable_d([[BODY[k]] for k in ('Ls', 'Rs', 'Le', 'Re', 'Lh', 'Rh', 'Lk', 'Rk', 'La', 'Ra')], camC, FR, origin)
    def dots(d):
        out = ''
        for seg in d.split('M')[1:]:
            x, y = seg.strip().split(' ')[:2]
            out += f'M{x} {y} m-3 0 a3 3 0 1 0 6 0 a3 3 0 1 0 -6 0'
        return out
    jdd = [dots(d) for d in jd]
    b += f'<path d="{jdd[0]}" fill="{T["faint"]}" stroke="{T["ink"]}" stroke-width="1.2"><animate attributeName="d" values="{";".join(jdd + [jdd[0]])}" dur="{DUR}s" repeatCount="indefinite"/></path>'
    b += f'<text x="410" y="470" class="serif mute" font-size="14" font-style="italic">surface vertices, drawn as rings</text>'
    b += f'<text x="810" y="470" class="serif mute" font-size="14" font-style="italic">bones, joints and <tspan fill="{T["acc"]}">muscle paths</tspan></text>'
    save(f'recon-{TN}.svg', svg(W, H, b))


# ------------------------------------------------------------------ AR glasses
def rrect(cx, cy, w, h, r, z, n=10):
    pts = []
    for (qx, qy, a0) in ((cx + w / 2 - r, cy + h / 2 - r, 0), (cx - w / 2 + r, cy + h / 2 - r, 90), (cx - w / 2 + r, cy - h / 2 + r, 180), (cx + w / 2 - r, cy - h / 2 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((qx + r * math.cos(a), qy + r * math.sin(a), z))
    pts.append(pts[0])
    return pts


def glasses_model():
    polys = {'frame': [], 'thin': [], 'display': [], 'grating': []}
    for sx in (-1, 1):
        cx = 33 * sx
        polys['frame'] += [rrect(cx, 0, 56, 44, 16, 0), rrect(cx, 0, 47, 35, 12, 0), rrect(cx, 0, 56, 44, 16, -5)]
        polys['thin'] += [rrect(cx, 0, 47, 35, 12, -5)]
        hx = 61 * sx
        polys['frame'] += [[(hx, 14, 0), (hx + 6 * sx, 14, -6), (hx + 7 * sx, 14, -12)], [(hx, -2, 0), (hx + 6 * sx, -2, -6), (hx + 7 * sx, -2, -12)]]
        tx = hx + 7 * sx
        top = [(tx, 14, -12), (tx + sx, 13, -70), (tx + 1.5 * sx, 11, -112), (tx + sx, 6, -128), (tx, -10, -150), (tx - sx, -24, -160)]
        bot = [(tx, -2, -12), (tx + sx, -3, -70), (tx + 1.5 * sx, -4, -104), (tx + sx, -8, -118), (tx, -18, -140), (tx - sx, -28, -156)]
        polys['frame'] += [top, bot, [top[0], bot[0]], [top[2], bot[2]], [top[-1], bot[-1]]]
        polys['thin'] += [[(tx + 3 * sx, 14, -14), (tx + 4 * sx, 13, -70), (tx + 4.5 * sx, 11, -110)], [(tx + 3 * sx, -2, -14), (tx + 4 * sx, -3, -70), (tx + 4.5 * sx, -4, -104)]]
    polys['frame'] += [[(-8, 9, 0), (-4, 12, 0), (4, 12, 0), (8, 9, 0)], [(-8, 9, -5), (-4, 12, -5), (4, 12, -5), (8, 9, -5)]]
    polys['thin'] += [[(-9, -8, -6), (-11, -15, -10)], [(9, -8, -6), (11, -15, -10)]]
    polys['display'] += [rrect(-33, 2, 26, 20, 3, -2.5, 3)]
    polys['grating'] += [[(-45 + k * 2.2, -7, -2.5), (-45 + k * 2.2, 11, -2.5)] for k in range(11)]
    comps = [
        ((-33, 2, -2.5), 'Waveguide display', 'green microLED · 640 × 480'),
        ((57, 9, 1), 'Camera', '1080p photo and video'),
        ((-69, 0, -30), 'Microphone', '16 kHz · wake word on device'),
        ((69, 6, -45), 'ARM SoC, Wi-Fi and BT', 'seven static binaries'),
        ((69, 6, -80), 'Touch + capture keys', '2 touch · 1 mechanical'),
        ((-69, 6, -78), '6-axis IMU', 'head orientation'),
        ((-69, 6, -112), 'Battery', '3.7 V Li-po'),
    ]
    return polys, comps


def glasses():
    W, H = 1200, 420
    FR, DUR = 40, 12
    cam = Cam(yaw=0, pitch=22, dist=430, F=1000, cx=420, cy=225, target=(0, -2, -70))
    b = f'<text x="0" y="22" class="caps">A · CEREBEL GLASSES, LINE DRAWING</text><line x1="0" y1="34" x2="840" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="880" y="22" class="caps">B · WHAT THE WEARER SEES</text><line x1="880" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    polys, comps = glasses_model()
    yaws = [math.radians(-52 + 16 * math.sin(2 * math.pi * k / FR)) for k in range(FR)]
    def proj_frames(pl):
        out = []
        for a in yaws:
            parts = ''
            for poly in pl:
                q = [cam.p(rot(p, (0, 1, 0), a)) for p in poly]
                parts += 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in q)
            out.append(parts)
        return out
    for key, col, wd, op in (('thin', T['ink'], .8, .45), ('frame', T['ink'], 1.5, 1), ('display', T['acc'], 1.4, 1), ('grating', T['acc'], .8, .55)):
        ds = proj_frames(polys[key])
        fill = f'fill="{T["acc"]}" fill-opacity=".08"' if key == 'display' else 'fill="none"'
        b += f'<path d="{ds[0]}" {fill} stroke="{col}" stroke-opacity="{op}" stroke-width="{wd}" stroke-linejoin="round" stroke-linecap="round"><animate attributeName="d" values="{";".join(ds + [ds[0]])}" dur="{DUR}s" repeatCount="indefinite"/></path>'
    mid = math.radians(-52)
    items = [(cam.p(rot(p, (0, 1, 0), mid)), p, lab, sub) for p, lab, sub in comps]
    left = sorted([it for it in items if it[0][0] < 420], key=lambda it: it[0][1])
    right = sorted([it for it in items if it[0][0] >= 420], key=lambda it: it[0][1])
    def place(col, x_text, anchor):
        y = 70; out = ''
        for q, p, lab, sub in col:
            ty = max(y, q[1] - 10)
            xs = [f(cam.p(rot(p, (0, 1, 0), a))[0]) for a in yaws]; ys = [f(cam.p(rot(p, (0, 1, 0), a))[1]) for a in yaws]
            xv, yv = ';'.join(xs + [xs[0]]), ';'.join(ys + [ys[0]])
            lx = x_text + (8 if anchor == 'end' else -8)
            out += (f'<line x1="{lx}" y1="{f(ty-5)}" x2="{xs[0]}" y2="{ys[0]}" stroke="{T["mute"]}" stroke-width=".7">'
                    f'<animate attributeName="x2" values="{xv}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="y2" values="{yv}" dur="{DUR}s" repeatCount="indefinite"/></line>')
            out += (f'<circle r="2.6" fill="{T["acc"]}" cx="{xs[0]}" cy="{ys[0]}"><animate attributeName="cx" values="{xv}" dur="{DUR}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="cy" values="{yv}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
            out += f'<text x="{x_text}" y="{f(ty)}" font-size="14.5" font-weight="600" text-anchor="{anchor}">{lab}</text>'
            out += f'<text x="{x_text}" y="{f(ty+17)}" class="mono mute" font-size="12" text-anchor="{anchor}">{sub}</text>'
            y = ty + 56
        return out
    b += place(left, 238, 'end')
    b += place(right, 700, 'start')
    dx, dy, dw, dh = 880, 64, 320, 240
    g = '#5CFF8A'
    b += f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="10" fill="#050806" stroke="{T["hair"]}"/>'
    b += f'<text x="{dx+16}" y="{dy+28}" class="mono" font-size="13" fill="{g}" fill-opacity=".7">10:42</text>'
    b += f'<text x="{dx+dw-16}" y="{dy+28}" class="mono" font-size="13" fill="{g}" fill-opacity=".7" text-anchor="end">REC ●</text>'
    lines = [('“Hey Cerebel,', .05), ('how was that swing?”', .14), ('Lead knee 162°', .36), ('at impact.', .42), ('Stay flexed next rep.', .52)]
    for i, (txt, t) in enumerate(lines):
        big = i >= 2
        y = dy + 76 + i * 34 + (14 if big else 0)
        fs = 22 if big else 16
        b += (f'<text x="{dx+22}" y="{y}" class="mono" font-size="{fs}" fill="{g}" fill-opacity="{1 if big else .65}" opacity="0">{txt}'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t};{f(t+.02)};.92;1" dur="9s" repeatCount="indefinite"/></text>')
    for k in range(9):
        h = 6 + 10 * abs(math.sin(k * 1.3))
        b += (f'<rect x="{dx+dw-120+k*10}" y="{f(dy+dh-26-h/2)}" width="5" height="{f(h)}" rx="2" fill="{g}" fill-opacity=".7">'
              f'<animate attributeName="height" values="{f(h)};{f(h*.3)};{f(h)}" dur="{f(.7+k%4*.15)}s" repeatCount="indefinite"/></rect>')
    b += f'<text x="{dx+22}" y="{dy+dh-20}" class="mono" font-size="12" fill="{g}" fill-opacity=".55">listening</text>'
    b += f'<text x="{dx}" y="{dy+dh+26}" class="serif mute" font-size="14" font-style="italic">Drawn at the display’s native 640 × 480;</text>'
    b += f'<text x="{dx}" y="{dy+dh+46}" class="serif mute" font-size="14" font-style="italic">black is transparent on the waveguide.</text>'
    save(f'glasses-{TN}.svg', svg(W, H, b))
