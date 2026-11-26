"""3D figures (golf swing, tennis rally). Exec'd inside gen2.py so T, f, svg, save are in scope."""
import math


def v_add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def v_sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def v_mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)
def v_len(a): return math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2)
def v_unit(a): l = v_len(a) or 1; return v_mul(a, 1 / l)
def v_cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def v_dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def rot(v, axis, ang):
    k = v_unit(axis); c, s = math.cos(ang), math.sin(ang)
    return v_add(v_add(v_mul(v, c), v_mul(v_cross(k, v), s)), v_mul(k, v_dot(k, v) * (1 - c)))


class Cam:
    def __init__(self, yaw, pitch, dist, F, cx, cy, target=(0, 0, 0)):
        self.yaw, self.pitch, self.dist, self.F, self.cx, self.cy, self.t = math.radians(yaw), math.radians(pitch), dist, F, cx, cy, target

    def p(self, q):
        x, y, z = v_sub(q, self.t)
        cy_, sy_ = math.cos(self.yaw), math.sin(self.yaw)
        x, z = x * cy_ - z * sy_, x * sy_ + z * cy_
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        y, z = y * cp - z * sp, y * sp + z * cp
        d = self.dist - z
        return (self.cx + self.F * x / d, self.cy - self.F * y / d)


def smooth(u): return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ golf
GOLF_K = [  # hand angle a, club angle c, thorax rot, pelvis rot, lateral shift, name
    (0, 0, 0, 0, 0, 'address'), (55, 80, 38, 16, -.02, 'takeaway'), (128, 210, 88, 42, -.04, 'top'),
    (72, 60, 55, 30, .02, 'transition'), (0, 0, 18, 38, .05, 'impact'), (-95, -150, 62, 58, .08, 'release'),
    (-148, -235, 92, 75, .07, 'finish')]
GOLF_SEG = [1.0, 1.3, .55, .45, .5, .9]          # time between keyframes
GOLF_HOLD, GOLF_BACK = .9, 1.0                   # hold at finish, glide back to address


def golf_params(t):
    """t in absolute seconds within the loop -> param tuple (no name)."""
    acc = 0
    for i, d in enumerate(GOLF_SEG):
        if t <= acc + d:
            u = smooth((t - acc) / d)
            a, b = GOLF_K[i], GOLF_K[i + 1]
            return tuple(a[j] + (b[j] - a[j]) * u for j in range(5))
        acc += d
    if t <= acc + GOLF_HOLD:
        return GOLF_K[-1][:5]
    acc += GOLF_HOLD
    u = smooth(min(1, (t - acc) / GOLF_BACK))
    a, b = GOLF_K[-1], GOLF_K[0]
    return tuple(a[j] + (b[j] - a[j]) * u for j in range(5))


GOLF_SWING = sum(GOLF_SEG)
GOLF_LOOP = GOLF_SWING + GOLF_HOLD + GOLF_BACK


def golfer(params):
    a, c, sh, hp, lat = params
    up = (0, 1, 0)
    P = (lat, .95, 0)
    s = v_unit((0, math.cos(math.radians(33)), math.sin(math.radians(33))))
    S = v_add(P, v_mul(s, .5))
    shax = rot((1, 0, 0), s, -math.radians(sh))
    hpax = rot((1, 0, 0), up, -math.radians(hp))
    Lh, Rh = v_add(P, v_mul(hpax, .11)), v_sub(P, v_mul(hpax, .11))
    Ls, Rs = v_add(S, v_mul(shax, .19)), v_sub(S, v_mul(shax, .19))
    head = v_add(S, v_add(v_mul(s, .2), (0, .06, .05)))
    B = (0, .03, .95)
    C = v_add(S, (0, -.04, .02))
    u = v_unit(v_sub(B, C)); w = (-1, 0, 0)
    def plane(r, ang):
        ang = math.radians(ang)
        return v_add(C, v_add(v_mul(u, r * math.cos(ang)), v_mul(w, r * math.sin(ang))))
    hand = plane(.62, a)
    club = v_add(hand, v_add(v_mul(u, .82 * math.cos(math.radians(c))), v_mul(w, .82 * math.sin(math.radians(c)))))
    def elbow(sh_):
        m = v_mul(v_add(sh_, hand), .5); return v_add(m, (0, -.03, .03))
    La, Ra = (.2, .06, .0), (-.2, .06, .0)
    Lk = v_add(v_mul(v_add(Lh, La), .5), (.02 * hp / 75, 0, .09))
    Rk = v_add(v_mul(v_add(Rh, Ra), .5), (.05 * hp / 75, 0, .09 - .05 * hp / 75))
    Lt, Rt = v_add(La, (.03, -.05, .13)), v_add(Ra, (-.03, -.05, .13))
    fwd_p = v_cross(hpax, up)
    return dict(P=P, S=S, Lh=Lh, Rh=Rh, Ls=Ls, Rs=Rs, head=head, hand=hand, club=club, Le=elbow(Ls), Re=elbow(Rs),
                La=La, Ra=Ra, Lk=Lk, Rk=Rk, Lt=Lt, Rt=Rt, C=C, u=u, w=w, B=B, s=s, shax=shax, hpax=hpax, fwd_p=fwd_p)


GOLF_BONES = [('P', 'S', 2.6), ('Ls', 'Rs', 2.4), ('Lh', 'Rh', 2.4), ('Ls', 'Le', 2.2), ('Le', 'hand', 2), ('Rs', 'Re', 2.2), ('Re', 'hand', 2),
              ('Lh', 'Lk', 2.6), ('Lk', 'La', 2.2), ('La', 'Lt', 1.8), ('Rh', 'Rk', 2.6), ('Rk', 'Ra', 2.2), ('Ra', 'Rt', 1.8), ('S', 'head', 2)]


def golf3d():
    W, H = 1200, 470
    cam = Cam(yaw=-40, pitch=16, dist=5.4, F=720, cx=300, cy=262, target=(0, .8, .3))
    b = f'<text x="0" y="22" class="caps">A · 3D RECONSTRUCTION, OBLIQUE VIEW</text><line x1="0" y1="34" x2="560" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="610" y="22" class="caps">B · SEGMENT ROTATION ABOUT THE VERTICAL AXIS</text><line x1="610" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    # clip for left panel
    b += '<clipPath id="lp"><rect x="0" y="40" width="570" height="420"/></clipPath><g clip-path="url(#lp)">'
    # floor grid
    for i in range(-6, 7):
        x = i * .25
        p1, p2 = cam.p((x, 0, -1.2)), cam.p((x, 0, 1.6))
        b += f'<line x1="{f(p1[0])}" y1="{f(p1[1])}" x2="{f(p2[0])}" y2="{f(p2[1])}" stroke="{T["hair"]}" stroke-width="{.9 if i == 0 else .6}"/>'
    for j in range(-4, 7):
        z = j * .25 + -.2
        p1, p2 = cam.p((-1.5, 0, z)), cam.p((1.5, 0, z))
        b += f'<line x1="{f(p1[0])}" y1="{f(p1[1])}" x2="{f(p2[0])}" y2="{f(p2[1])}" stroke="{T["hair"]}" stroke-width=".6"/>'
    # target line through ball
    g0 = golfer(GOLF_K[0][:5])
    t1, t2 = cam.p((-1.5, 0, g0['B'][2])), cam.p((1.6, 0, g0['B'][2]))
    b += f'<line x1="{f(t1[0])}" y1="{f(t1[1])}" x2="{f(t2[0])}" y2="{f(t2[1])}" stroke="{T["acc2"]}" stroke-width="1.1" stroke-dasharray="5 4" marker-end="url(#arr)"/>'
    b += f'<text x="{f(t2[0]-6)}" y="{f(t2[1]+18)}" class="serif" font-size="14" font-style="italic" fill="{T["acc2"]}" text-anchor="end">target line</text>'
    # swing plane (disc through shoulder centre containing ball direction and target line)
    C, u, w = g0['C'], g0['u'], g0['w']
    pts = [cam.p(v_add(C, v_add(v_mul(u, 1.44 * math.cos(k / 72 * 2 * math.pi)), v_mul(w, 1.44 * math.sin(k / 72 * 2 * math.pi))))) for k in range(73)]
    b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in pts)}Z" fill="{T["acc"]}" fill-opacity=".05" stroke="{T["acc"]}" stroke-opacity=".35" stroke-width=".8"/>'
    lab = pts[20]
    b += f'<text x="{f(lab[0]+4)}" y="{f(lab[1]-6)}" class="serif" font-size="14" font-style="italic" fill="{T["acc"]}">swing plane</text>'
    # ball
    bp = cam.p(g0['B'])
    b += f'<circle cx="{f(bp[0])}" cy="{f(bp[1])}" r="3.2" fill="{T["ink"]}"/>'
    # frames
    N = 110
    times = [GOLF_LOOP * k / (N - 1) for k in range(N)]
    G = [golfer(golf_params(t)) for t in times]
    # clubhead trajectory (swing only)
    tr = [cam.p(golfer(golf_params(GOLF_SWING * k / 200))['club']) for k in range(201)]
    b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in tr)}" fill="none" stroke="{T["acc"]}" stroke-opacity=".55" stroke-width="1" stroke-dasharray="1.5 3"/>'
    def anim_line(key_a, key_b, color, width, opacity=1, shadow=False):
        def P(g, k):
            q = g[k]
            return cam.p((q[0], 0.001, q[2])) if shadow else cam.p(q)
        vals = {att: [] for att in ('x1', 'y1', 'x2', 'y2')}
        for g in G:
            a_, z_ = P(g, key_a), P(g, key_b)
            vals['x1'].append(f(a_[0])); vals['y1'].append(f(a_[1])); vals['x2'].append(f(z_[0])); vals['y2'].append(f(z_[1]))
        an = ''.join(f'<animate attributeName="{k}" dur="{GOLF_LOOP}s" repeatCount="indefinite" values="{";".join(v)}"/>' for k, v in vals.items())
        return (f'<line x1="{vals["x1"][0]}" y1="{vals["y1"][0]}" x2="{vals["x2"][0]}" y2="{vals["y2"][0]}" stroke="{color}" '
                f'stroke-opacity="{opacity}" stroke-width="{width}" stroke-linecap="round">{an}</line>')
    def anim_dot(key, r, fill, stroke=None):
        xs = ';'.join(f(cam.p(g[key])[0]) for g in G); ys = ';'.join(f(cam.p(g[key])[1]) for g in G)
        st = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
        return (f'<circle r="{r}" fill="{fill}"{st} cx="{xs.split(";")[0]}" cy="{ys.split(";")[0]}">'
                f'<animate attributeName="cx" dur="{GOLF_LOOP}s" repeatCount="indefinite" values="{xs}"/>'
                f'<animate attributeName="cy" dur="{GOLF_LOOP}s" repeatCount="indefinite" values="{ys}"/></circle>')
    # shadow on floor
    for a_, z_, wd in GOLF_BONES + [('hand', 'club', 1.4)]:
        b += anim_line(a_, z_, T['ink'], wd + 2, .07, shadow=True)
    # segment frames: add virtual endpoints
    for g in G:
        g['Px'] = v_add(g['P'], v_mul(g['hpax'], .16)); g['Pz'] = v_add(g['P'], v_mul(g['fwd_p'], .16)); g['Py'] = v_add(g['P'], (0, .16, 0))
        fz = v_cross(g['shax'], g['s'])
        g['Sx'] = v_add(g['S'], v_mul(g['shax'], .3)); g['Sz'] = v_add(g['S'], v_mul(fz, -.16))
    # far side first (right side of body), then near side
    for a_, z_, wd in GOLF_BONES:
        far = a_.startswith('R') or z_.startswith('R')
        b += anim_line(a_, z_, T['ink'], wd, .45 if far else 1)
    b += anim_line('hand', 'club', T['acc'], 1.6)
    b += anim_line('P', 'Px', T['acc2'], 1.4); b += anim_line('P', 'Pz', T['acc2'], 1.4, .6)
    b += anim_line('S', 'Sx', T['acc'], 1.4); b += anim_line('S', 'Sz', T['acc'], 1.4, .6)
    for k in ('Ls', 'Rs', 'Le', 'Re', 'hand', 'Lh', 'Rh', 'Lk', 'Rk', 'La', 'Ra'):
        b += anim_dot(k, 2.6, T['ink'])
    b += anim_dot('head', 10, 'none', T['ink'])
    b += anim_dot('club', 3, T['acc'])
    b += '</g>'
    # legends for frames
    b += f'<line x1="0" y1="452" x2="18" y2="452" stroke="{T["acc2"]}" stroke-width="1.6"/><text x="24" y="457" class="serif ink2" font-size="14">pelvis frame</text>'
    b += f'<line x1="130" y1="452" x2="148" y2="452" stroke="{T["acc"]}" stroke-width="1.6"/><text x="154" y="457" class="serif ink2" font-size="14">thorax frame</text>'
    # ----- plot
    px0, px1, py0, py1 = 660, 1150, 76, 400
    names = [k[5] for k in GOLF_K]
    ktimes = [0]
    for d in GOLF_SEG: ktimes.append(ktimes[-1] + d)
    X = lambda t: px0 + (px1 - px0) * t / GOLF_SWING
    Y = lambda v: py1 - (v + 10) / 110 * (py1 - py0)
    for i in range(len(ktimes) - 1):
        if i % 2 == 0:
            b += f'<rect x="{f(X(ktimes[i]))}" y="{py0}" width="{f(X(ktimes[i+1])-X(ktimes[i]))}" height="{py1-py0}" fill="{T["faint"]}"/>'
    for v in (0, 30, 60, 90):
        b += f'<line x1="{px0}" y1="{f(Y(v))}" x2="{px1}" y2="{f(Y(v))}" stroke="{T["hair"]}" stroke-width="{1 if v == 0 else .5}"/><text x="{px0-8}" y="{f(Y(v)+4)}" class="mono mute" font-size="12" text-anchor="end">{v}°</text>'
    for t, nm in zip(ktimes, names):
        b += f'<line x1="{f(X(t))}" y1="{py1}" x2="{f(X(t))}" y2="{py1+5}" stroke="{T["mute"]}"/>{"" if nm in ("transition", "release") else f'<text x="{f(X(t))}" y="{py1+22}" class="serif mute" font-size="13.5" font-style="italic" text-anchor="middle">{nm}</text>'}'
    M = 240
    ts = [GOLF_SWING * k / M for k in range(M + 1)]
    th = [(X(t), Y(golf_params(t)[2])) for t in ts]
    pv = [(X(t), Y(golf_params(t)[3])) for t in ts]
    band = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in th) + ' L' + ' L'.join(f'{f(x)} {f(y)}' for x, y in reversed(pv)) + 'Z'
    b += f'<path d="{band}" fill="{T["acc"]}" fill-opacity=".13"/>'
    for pts_, col, nm in ((th, T['ink'], 'thorax'), (pv, T['acc2'], 'pelvis')):
        d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts_)
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8"/>'
        end = pts_[-1]
        b += f'<text x="{f(end[0]-4)}" y="{f(end[1]-10 if nm == "thorax" else end[1]+20)}" class="serif" font-size="15" font-style="italic" fill="{col}" text-anchor="end">{nm}</text>'
    # X-factor annotation at top
    tt = ktimes[2]; xt = X(tt); yth = Y(GOLF_K[2][2]); ypv = Y(GOLF_K[2][3])
    b += f'<line x1="{f(xt)}" y1="{f(yth)}" x2="{f(xt)}" y2="{f(ypv)}" stroke="{T["acc"]}" stroke-width="1.2"/>'
    b += f'<line x1="{f(xt-4)}" y1="{f(yth)}" x2="{f(xt+4)}" y2="{f(yth)}" stroke="{T["acc"]}"/><line x1="{f(xt-4)}" y1="{f(ypv)}" x2="{f(xt+4)}" y2="{f(ypv)}" stroke="{T["acc"]}"/>'
    b += f'<text x="{f(xt+10)}" y="{f((yth+ypv)/2+5)}" class="serif" font-size="15" font-style="italic" fill="{T["acc"]}">X-factor {GOLF_K[2][2]-GOLF_K[2][3]}°</text>'
    # synced cursor + dots
    fr = GOLF_SWING / GOLF_LOOP
    kt = f'0;{f(fr)};{f(min(fr + GOLF_HOLD / GOLF_LOOP, .999))};1'
    b += (f'<line x1="{px0}" y1="{py0}" x2="{px0}" y2="{py1}" stroke="{T["ink"]}" stroke-opacity=".55" stroke-width=".8">'
          f'<animate attributeName="x1" values="{px0};{px1};{px1};{px0}" keyTimes="{kt}" dur="{GOLF_LOOP}s" repeatCount="indefinite"/>'
          f'<animate attributeName="x2" values="{px0};{px1};{px1};{px0}" keyTimes="{kt}" dur="{GOLF_LOOP}s" repeatCount="indefinite"/>'
          f'<animate attributeName="stroke-opacity" values=".55;.55;.55;0" keyTimes="{kt}" dur="{GOLF_LOOP}s" repeatCount="indefinite"/></line>')
    # dots: sample same loop timing
    for idx, col in ((2, T['ink']), (3, T['acc2'])):
        xs, ys = [], []
        for t in times:
            tc = min(t, GOLF_SWING) if t <= GOLF_SWING + GOLF_HOLD else GOLF_SWING * (1 - (t - GOLF_SWING - GOLF_HOLD) / GOLF_BACK)
            xs.append(f(X(tc))); ys.append(f(Y(golf_params(tc)[idx])))
        b += (f'<circle r="3.6" fill="{col}" cx="{xs[0]}" cy="{ys[0]}"><animate attributeName="cx" dur="{GOLF_LOOP}s" repeatCount="indefinite" values="{";".join(xs)}"/>'
              f'<animate attributeName="cy" dur="{GOLF_LOOP}s" repeatCount="indefinite" values="{";".join(ys)}"/></circle>')
    save(f'golf-{TN}.svg', svg(W, H, b))


# ------------------------------------------------------------------ tennis
def tennis():
    W, H = 1200, 470
    cam = Cam(yaw=0, pitch=30, dist=44, F=900, cx=300, cy=236, target=(0, 0, -.5))
    b = f'<text x="0" y="22" class="caps">A · BALL TRACK ON A CALIBRATED COURT</text><line x1="0" y1="34" x2="600" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="680" y="22" class="caps">B · BOUNCE MAP, TOP-DOWN</text><line x1="680" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    hw, sw, hl, sl = 5.485, 4.115, 11.885, 6.4
    def L(a, c, col=None, wd=1.1, op=1):
        p, q = cam.p(a), cam.p(c)
        return f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="{col or T["ink2"]}" stroke-width="{wd}" stroke-opacity="{op}"/>'
    # court surface
    corners = [cam.p(q) for q in ((-hw, 0, -hl), (hw, 0, -hl), (hw, 0, hl), (-hw, 0, hl))]
    b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in corners)}Z" fill="{T["faint"]}"/>'
    for x in (-hw, hw, -sw, sw):
        b += L((x, 0, -hl), (x, 0, hl))
    for z in (-hl, hl):
        b += L((-hw, 0, z), (hw, 0, z))
    for z in (-sl, sl):
        b += L((-sw, 0, z), (sw, 0, z))
    b += L((0, 0, -sl), (0, 0, sl))
    for z in (-hl, hl):
        b += L((0, 0, z), (0, 0, z + (.2 if z < 0 else -.2)))
    # homography corner markers
    for q in ((-hw, 0, -hl), (hw, 0, -hl), (hw, 0, hl), (-hw, 0, hl)):
        p = cam.p(q)
        b += f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="5" fill="none" stroke="{T["acc2"]}" stroke-width="1.2"/>'
    p = cam.p((hw, 0, -hl))
    b += f'<text x="{f(p[0]+12)}" y="{f(p[1]+5)}" class="serif" font-size="14" font-style="italic" fill="{T["acc2"]}">homography keypoints</text>'
    # rally: list of (hit point, bounce point) alternating ends
    shots = [((-1.5, 1.0, 12.2), (2.6, 0, -8.6)), ((2.4, .9, -12.6), (-3.1, 0, 9.4)), ((-3.0, 1.1, 12.4), (-0.6, 0, -5.4)),
             ((-0.8, .8, -11.6), (3.4, 0, 7.9))]
    seq = []   # 3D samples uniform in time
    bounces = []
    for i, (hit, bnc) in enumerate(shots):
        nxt = shots[i + 1][0] if i + 1 < len(shots) else (bnc[0] * 1.15, .9, bnc[2] * 1.45)
        for k in range(28):            # hit -> bounce, peak above net
            u = k / 28
            x = hit[0] + (bnc[0] - hit[0]) * u; z = hit[2] + (bnc[2] - hit[2]) * u
            y = hit[1] * (1 - u) + 4 * 1.6 * u * (1 - u) + 0
            seq.append((x, max(y, 0), z))
        bounces.append((len(seq), bnc))
        for k in range(16):            # bounce -> next hit
            u = k / 16
            x = bnc[0] + (nxt[0] - bnc[0]) * u; z = bnc[2] + (nxt[2] - bnc[2]) * u
            y = nxt[1] * u + 4 * .9 * u * (1 - u)
            seq.append((x, y, z))
    n = len(seq); DUR = 7.5
    proj = [cam.p(q) for q in seq]; shad = [cam.p((q[0], 0, q[2])) for q in seq]
    path = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in proj)
    b += f'<path d="{path}" fill="none" stroke="{T["acc"]}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="1.5 3"/>'
    # net (drawn after the far half of the track so it occludes nothing important)
    for x0, x1 in ((-hw - .9, hw + .9),):
        a1, a2, a3, a4 = cam.p((x0, 0, 0)), cam.p((x1, 0, 0)), cam.p((x1, 1.07, 0)), cam.p((x0, 1.07, 0))
        b += f'<path d="M{f(a1[0])} {f(a1[1])} L{f(a2[0])} {f(a2[1])} L{f(a3[0])} {f(a3[1])} L{f(a4[0])} {f(a4[1])}Z" fill="{T["ink"]}" fill-opacity=".06" stroke="{T["ink2"]}" stroke-width="1"/>'
    for idx, bnc in bounces:
        p = cam.p(bnc); t = idx / n
        b += (f'<ellipse cx="{f(p[0])}" cy="{f(p[1])}" rx="7" ry="3" fill="none" stroke="{T["acc"]}" stroke-width="1.4" opacity="0">'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(t-.001)};{f(t)};.97;1" dur="{DUR}s" repeatCount="indefinite"/></ellipse>')
    xs = ';'.join(f(p[0]) for p in proj); ys = ';'.join(f(p[1]) for p in proj)
    sx = ';'.join(f(p[0]) for p in shad); sy = ';'.join(f(p[1]) for p in shad)
    rs = ';'.join(f(max(2.2, 900 * .12 / (44 - (q[1] * math.sin(math.radians(30)) + (q[2] + .5) * math.cos(math.radians(30)))))) for q in seq)
    b += (f'<ellipse rx="4" ry="1.6" fill="{T["ink"]}" fill-opacity=".25"><animate attributeName="cx" values="{sx}" dur="{DUR}s" repeatCount="indefinite"/>'
          f'<animate attributeName="cy" values="{sy}" dur="{DUR}s" repeatCount="indefinite"/></ellipse>')
    b += (f'<circle r="3" fill="{T["acc"]}"><animate attributeName="cx" values="{xs}" dur="{DUR}s" repeatCount="indefinite"/>'
          f'<animate attributeName="cy" values="{ys}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="r" values="{rs}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    # ---- top-down bounce map
    ox, oy, sc = 945, 240, 18   # centre, px per metre (z -> x horizontal)
    def TD(x, z): return ox + z * sc, oy + x * sc
    def TL(a, c):
        p, q = TD(*a), TD(*c)
        return f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="{T["ink2"]}" stroke-width="1"/>'
    c1, c2 = TD(-hw, -hl), TD(hw, hl)
    b += f'<rect x="{f(c1[0])}" y="{f(c1[1])}" width="{f(c2[0]-c1[0])}" height="{f(c2[1]-c1[1])}" fill="{T["faint"]}"/>'
    for x in (-hw, hw, -sw, sw): b += TL((x, -hl), (x, hl))
    for z in (-hl, hl): b += TL((-hw, z), (hw, z))
    for z in (-sl, sl): b += TL((-sw, z), (sw, z))
    b += TL((0, -sl), (0, sl))
    n1, n2 = TD(-hw - .9, 0), TD(hw + .9, 0)
    b += f'<line x1="{f(n1[0])}" y1="{f(n1[1])}" x2="{f(n2[0])}" y2="{f(n2[1])}" stroke="{T["ink"]}" stroke-width="1.6"/>'
    rnd = __import__('random').Random(5)
    for k in range(70):
        side = 1 if k % 2 else -1
        depth = min(hl - .2, max(1.5, rnd.gauss(8.6, 1.8)))
        x = max(-sw + .1, min(sw - .1, rnd.gauss(0, 2.0)))
        p = TD(x, side * depth)
        b += f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="2.6" fill="{T["acc"]}" fill-opacity=".55"/>'
    for idx, bnc in bounces:
        p = TD(bnc[0], bnc[2])
        b += f'<circle cx="{f(p[0])}" cy="{f(p[1])}" r="5.5" fill="none" stroke="{T["ink"]}" stroke-width="1.3"/>'
    b += f'<text x="{f(c1[0])}" y="{f(c2[1]+28)}" class="serif ink2" font-size="14"><tspan fill="{T["acc"]}">●</tspan> bounces in one session   <tspan font-weight="700">○</tspan> the rally on the left</text>'
    save(f'tennis-{TN}.svg', svg(W, H, b))
