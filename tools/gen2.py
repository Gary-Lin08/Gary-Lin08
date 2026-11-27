"""Editorial, paper-style figures for Gary-Lin08's GitHub profile and repos.

Every figure is rendered twice (light / dark) with a transparent background so it
sits on GitHub's page like a figure in a paper. Use <picture> with
prefers-color-scheme to pick the variant.
"""
import math, os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',Georgia,serif"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Mono',Consolas,Menlo,monospace"

THEMES = {
    'light': dict(ink='#1F2328', ink2='#424A53', mute='#6E7781', hair='#D0D7DE', faint='#F3F5F7',
                  acc='#B4461A', acc2='#2F5D8A', acc3='#6B7A38'),
    'dark': dict(ink='#E6EDF3', ink2='#C2CAD3', mute='#8B949E', hair='#3A414A', faint='#161B22',
                 acc='#E58A55', acc2='#86ACD6', acc3='#AFBF72'),
}
T = THEMES['light']


def f(x):
    s = f"{x:.4f}" if abs(x) < 1 else f"{x:.1f}"
    s = s.rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'


def svg(w, h, body, defs=''):
    css = f"""
text{{font-family:{SANS};}} text:not([fill]){{fill:{T['ink']};}}
.serif{{font-family:{SERIF};}} .mono{{font-family:{MONO};}}
text.caps{{letter-spacing:.14em;font-size:13px;fill:{T['mute']};}}
text.ink2{{fill:{T['ink2']};}} text.mute{{fill:{T['mute']};}} text.acc{{fill:{T['acc']};}}
"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs><style>{css}</style>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1.5 L9 5 L0 8.5" fill="none" stroke="{T['mute']}" stroke-width="1.4"/></marker>
{defs}</defs>
{body}
</svg>'''


CAPTIONS = {
    'glasses': (1, 'The Cerebel glasses, rendered from the production CAD.', 'The grating layout on the lens is schematic.'),
    'system': (2, 'System overview.', 'Video and kinematics in orange, audio in blue, retrieval in green.'),
    'recon': (3, 'One recorded session, three views.', 'A: 77 body joints estimated by GEM-X from a phone video. B: the same motion solved by OpenSim inverse kinematics on the Rajagopal musculoskeletal model (Rajagopal et al. 2016; Lai et al. 2017; Uhlrich et al. 2022), drawn with its bone geometry and 80 muscle paths. C: four of the resulting joint angles.'),
    'golf': (4, 'A golf swing in 3D.', 'Pelvis and thorax rotation about the vertical axis; the shaded gap between them is the X-factor. Illustrative data.'),
    'wake': (5, 'Hey Cerebel keyword spotting.', 'Waveform, 40-band log-mel features, a TC-ResNet, and the two-frame decision rule.'),
    'results': (6, 'Wake-word accuracy on held-out speakers.', 'v2 is trained only on commercially licensed voices.'),
    'tennis': (7, 'Ball tracking on a calibrated court.', 'Four keypoints fix the court homography, and each bounce is projected onto the ground plane. Illustrative rally and bounce map.'),
    'tmodel': (8, 'The Tennis AI model stack.', '(a) GridTrackNet takes five frames and predicts a coarse confidence grid with sub-cell offsets. (b) A homography from four court keypoints maps detections to metres. (c) Bounces are sign flips of vertical velocity. (d) MoveNet gives 17 keypoints per frame. (e) A GRU classifies 30-frame pose windows into four classes (probabilities shown are illustrative). (f) A state machine turns events into rallies and a score.'),
}


def _wrap(text, n):
    out, cur = [], ''
    for w in text.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur: out.append(cur)
    return out


def save(name, content):
    key = name.rsplit('-', 1)[0]
    if key in CAPTIONS:
        import re as _re
        num, title, rest = CAPTIONS[key]
        m = _re.search(r'width="(\d+)" height="(\d+)" viewBox="0 0 (\d+) (\d+)"', content)
        w, h = int(m.group(1)), int(m.group(2))
        lines = _wrap(rest, 118) if rest else []
        y = h + 30
        cap = f'<text x="0" y="{y}" class="serif" font-size="18"><tspan font-weight="700">Figure {num}.</tspan> <tspan font-style="italic">{title}</tspan></text>'
        for i, ln in enumerate(lines):
            cap += f'<text x="0" y="{y + 26 * (i + 1)}" class="serif ink2" font-size="17">{ln}</text>'
        nh = y + 26 * len(lines) + 14
        content = content.replace(m.group(0), f'width="{w}" height="{nh}" viewBox="0 0 {w} {nh}"', 1)
        content = content.replace('</svg>', cap + '\n</svg>')
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        fh.write(content)


def caption(x, y, num, title, rest, w=None):
    return ''
    s = f'<text x="{x}" y="{y}" class="serif" font-size="16"><tspan font-weight="700">Figure {num}.</tspan> <tspan font-style="italic">{title}</tspan></text>'
    if rest:
        s += f'<text x="{x}" y="{y+20}" class="serif ink2" font-size="15.5">{rest}</text>'
    return s


def node(x, y, w, h, label, sub=None, emph=False):
    stroke = T['acc'] if emph else T['hair']
    s = f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="5" fill="{T["faint"]}" stroke="{stroke}" stroke-width="1"/>'
    ty = y + h / 2 + (-2 if sub else 4.5)
    s += f'<text x="{f(x+12)}" y="{f(ty)}" font-size="15" font-weight="600">{label}</text>'
    if sub:
        s += f'<text x="{f(x+12)}" y="{f(ty+16)}" class="mono mute" font-size="12.5">{sub}</text>'
    return s


def curve(x1, y1, x2, y2, bend=.5):
    dx = (x2 - x1) * bend
    return f'M{f(x1)} {f(y1)} C{f(x1+dx)} {f(y1)} {f(x2-dx)} {f(y2)} {f(x2)} {f(y2)}'


def relay(paths, period, color=None, r=3.2):
    """One dot that hops edge to edge: path i is travelled during its own time slice."""
    color = color or T['acc']
    n = len(paths)
    s = ''
    for i, (pid, d) in enumerate(paths):
        a, b = i / n, (i + 1) / n
        a2, b2 = max(a, 0.0001), min(b, .9999)
        s += (f'<circle r="{r}" fill="{color}" opacity="0">'
              f'<animateMotion dur="{period}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;{f(a2)};{f(b2)};1" calcMode="linear"><mpath xlink:href="#{pid}"/></animateMotion>'
              f'<animate attributeName="opacity" dur="{period}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{f(a2)};{f(a2+.001)};{f(b2-.001)};{f(b2)};1"/></circle>')
    return s


# ------------------------------------------------------------------ figures

def stick_run(phase, x, y0=0):
    """Sagittal running pose. phase in cycles. returns dict of joints."""
    p = 2 * math.pi * phase
    bob = 3 * math.cos(2 * p)
    hip = (x, y0 + bob)
    lean = math.radians(9)
    sh = (hip[0] + 58 * math.sin(lean), hip[1] - 58 * math.cos(lean))
    head = (sh[0] + 15 * math.sin(lean), sh[1] - 17)

    def leg(ph):
        th = math.radians(24 * math.sin(ph))
        kf = math.radians(14 + 92 * max(0, math.cos(ph)) ** 2 + 26 * max(0, -math.cos(ph)) ** 2)
        knee = (hip[0] + 46 * math.sin(th), hip[1] + 46 * math.cos(th))
        sa = th - kf
        ank = (knee[0] + 46 * math.sin(sa), knee[1] + 46 * math.cos(sa))
        toe = (ank[0] + 10, ank[1] + 1.5)
        return knee, ank, toe

    def arm(ph):
        a = math.radians(-34 * math.sin(ph))
        el = (sh[0] + 29 * math.sin(a), sh[1] + 29 * math.cos(a))
        fa = a + math.radians(85)
        wr = (el[0] + 26 * math.sin(fa), el[1] + 26 * math.cos(fa))
        return el, wr
    kL, aL, tL = leg(p); kR, aR, tR = leg(p + math.pi)
    eL, wL = arm(p); eR, wR = arm(p + math.pi)
    return dict(hip=hip, sh=sh, head=head, kL=kL, aL=aL, tL=tL, kR=kR, aR=aR, tR=tR, eL=eL, wL=wL, eR=eR, wR=wR)


RUN_BONES = [('hip', 'sh'), ('sh', 'head'), ('hip', 'kL'), ('kL', 'aL'), ('aL', 'tL'), ('hip', 'kR'), ('kR', 'aR'), ('aR', 'tR'),
             ('sh', 'eL'), ('eL', 'wL'), ('sh', 'eR'), ('eR', 'wR')]


def header():
    W, H = 1200, 310
    b = ''
    # typography block
    b += f'<text x="0" y="104" class="serif" font-size="74" letter-spacing="-.5">Kaijun Lin</text>'
    b += f'<line x1="2" y1="164" x2="520" y2="164" stroke="{T["hair"]}"/>'
    b += f'<text x="2" y="198" class="serif ink2" font-size="21">Building <tspan font-style="italic" fill="{T["ink"]}">Cerebel AI</tspan>, wearable perception</text>'
    b += f'<text x="2" y="226" class="serif ink2" font-size="21">that understands how people move.</text>'
    b += f'<text x="2" y="266" class="mono" font-size="14" fill="{T["acc"]}">cerebel.tech</text>'
    b += f'<text x="112" y="266" class="mono mute" font-size="14">·  Wearable Motion Intelligence</text>'
    # chronophotograph
    gy = 236
    X0, X1 = 600, 1170
    steps = 9
    stride = (X1 - X0) / (steps - 1)
    cyc_per_img = .23

    def P(xpos):
        ph = (xpos - X0) / stride * cyc_per_img
        return stick_run(ph, xpos, gy - 86)
    b += f'<line x1="{X0-40}" y1="{gy+1}" x2="{X1+28}" y2="{gy+1}" stroke="{T["hair"]}"/>'
    for i in range(steps):
        p = P(X0 + i * stride)
        op = .16 + .2 * (i % 2)
        for a, z in RUN_BONES:
            b += f'<line x1="{f(p[a][0])}" y1="{f(p[a][1])}" x2="{f(p[z][0])}" y2="{f(p[z][1])}" stroke="{T["ink"]}" stroke-opacity="{f(op)}" stroke-width="1.4" stroke-linecap="round"/>'
        b += f'<circle cx="{f(p["head"][0])}" cy="{f(p["head"][1])}" r="7.5" fill="none" stroke="{T["ink"]}" stroke-opacity="{f(op)}" stroke-width="1.4"/>'
    # tick marks / time stamps
    for i in range(steps):
        x = X0 + i * stride
        b += f'<line x1="{f(x)}" y1="{gy+6}" x2="{f(x)}" y2="{gy+11}" stroke="{T["mute"]}"/>'
        if i % 2 == 0:
            b += f'<text x="{f(x)}" y="{gy+26}" class="mono mute" font-size="12" text-anchor="middle">{i*50} ms</text>'
    # animated runner in accent
    N = 72
    xs = [X0 + (X1 - X0) * k / (N - 1) for k in range(N)]
    poses = [P(x) for x in xs]
    DUR = 7
    op_vals = ';'.join('0' if k in (0, N - 1) else '1' for k in range(N))
    run = ''
    for a, z in RUN_BONES:
        anim = ''
        for att, key, idx in (('x1', a, 0), ('y1', a, 1), ('x2', z, 0), ('y2', z, 1)):
            anim += f'<animate attributeName="{att}" dur="{DUR}s" repeatCount="indefinite" values="{";".join(f(p[key][idx]) for p in poses)}"/>'
        run += f'<line stroke="{T["acc"]}" stroke-width="2.2" stroke-linecap="round" x1="{f(poses[0][a][0])}" y1="{f(poses[0][a][1])}" x2="{f(poses[0][z][0])}" y2="{f(poses[0][z][1])}">{anim}</line>'
    run += (f'<circle r="7.5" fill="none" stroke="{T["acc"]}" stroke-width="2.2" cx="{f(poses[0]["head"][0])}" cy="{f(poses[0]["head"][1])}">'
            f'<animate attributeName="cx" dur="{DUR}s" repeatCount="indefinite" values="{";".join(f(p["head"][0]) for p in poses)}"/>'
            f'<animate attributeName="cy" dur="{DUR}s" repeatCount="indefinite" values="{";".join(f(p["head"][1]) for p in poses)}"/></circle>')
    # trail of the ankle in accent
    trail = 'M' + ' L'.join(f'{f(p["aL"][0])} {f(p["aL"][1])}' for p in poses)
    b += f'<path d="{trail}" fill="none" stroke="{T["acc"]}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="1.5 3.5"/>'
    b += f'<g><animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.04;.95;1"/>{run}</g>'
    b += f'<text x="{X1+28}" y="{gy+54}" class="serif mute" font-size="14" font-style="italic" text-anchor="end">One running stride in nine phases, after É.-J. Marey’s chronophotographs</text>'
    save(f'header-{TN}.svg', svg(W, H, b))


def system():
    W, H = 1200, 400
    b = ''
    cols = [(0, 330, 'EDGE · AR GLASSES'), (380, 220, 'PHONE'), (650, 550, 'CLOUD')]
    for x, w, name in cols:
        b += f'<text x="{x}" y="22" class="caps">{name}</text><line x1="{x}" y1="34" x2="{x+w}" y2="34" stroke="{T["hair"]}"/>'
    N = {
        'mic': (0, 70, 138, 50, 'Microphone', '16 kHz audio'),
        'wake': (178, 70, 152, 50, 'Wake word', 'TC-ResNet, in C'),
        'cam': (0, 212, 138, 50, 'Camera', 'egocentric RGB'),
        'cap': (178, 212, 152, 50, 'Capture', 'encode · stream'),
        'app': (380, 141, 200, 50, 'iPhone app', 'BLE / Wi-Fi relay'),
        'ver': (380, 300, 200, 50, 'Second-pass verify', 'wake confirmation'),
        'pose': (650, 70, 176, 50, '3D pose and mesh', 'from plain video'),
        'ik': (650, 212, 176, 50, 'Musculoskeletal IK', 'OpenSim model'),
        'kin': (866, 212, 150, 50, 'Kinematics', 'angles · loads'),
        'kb': (866, 70, 150, 50, 'Sport packs', 'retrieval corpora'),
        'coach': (1056, 141, 144, 50, 'Coach', 'LLM + tools', True),
    }
    for k, v in N.items():
        b += node(*v[:6], emph=len(v) > 6)

    def R(k): x, y, w, h = N[k][:4]; return x + w, y + h / 2
    def L(k): x, y, w, h = N[k][:4]; return x, y + h / 2
    def Tp(k): x, y, w, h = N[k][:4]; return x + w / 2, y
    def B(k): x, y, w, h = N[k][:4]; return x + w / 2, y + h
    E = {
        'e_mw': curve(*R('mic'), *L('wake')), 'e_wa': curve(*R('wake'), L('app')[0] - 2, L('app')[1] - 8),
        'e_cc': curve(*R('cam'), *L('cap')), 'e_ca': curve(*R('cap'), L('app')[0] - 2, L('app')[1] + 8),
        'e_av': f'M{f(B("app")[0])} {f(B("app")[1])} L{f(Tp("ver")[0])} {f(Tp("ver")[1]-2)}',
        'e_ap': curve(*R('app'), L('pose')[0] - 2, L('pose')[1]),
        'e_pi': f'M{f(B("pose")[0])} {f(B("pose")[1])} L{f(Tp("ik")[0])} {f(Tp("ik")[1]-2)}',
        'e_ik': curve(*R('ik'), L('kin')[0] - 2, L('kin')[1]),
        'e_kc': curve(*R('kin'), L('coach')[0] - 2, L('coach')[1] + 8),
        'e_bc': curve(*R('kb'), L('coach')[0] - 2, L('coach')[1] - 8),
    }
    for pid, d in E.items():
        b += f'<path id="{pid}" d="{d}" fill="none" stroke="{T["mute"]}" stroke-width="1.1" marker-end="url(#arr)"/>'
    b += relay([(p, E[p]) for p in ('e_cc', 'e_ca', 'e_ap', 'e_pi', 'e_ik', 'e_kc')], 7)
    b += relay([(p, E[p]) for p in ('e_mw', 'e_wa', 'e_av')], 5.5, T['acc2'], 2.8)
    # coach output, set as a pull quote
    b += f'<line x1="650" y1="306" x2="650" y2="352" stroke="{T["acc"]}" stroke-width="2"/>'
    b += f'<text x="664" y="325" class="serif" font-size="17" font-style="italic">“Lead knee is at 162° at impact; stay flexed.”</text>'
    b += f'<text x="664" y="347" class="mono mute" font-size="12.5">the number comes from IK, not from the language model</text>'
    b += caption(0, 410, 1, 'The Cerebel stack, from a glance to a coaching cue.',
                 'Video (orange) is reconstructed into a musculoskeletal model in the cloud; audio (blue) is gated on the glasses by a 20k-parameter wake word.')
    save(f'system-{TN}.svg', svg(W, H, b))


def biomech():
    W, H = 1200, 432
    K = [(0, 0, 0, 0, 0, 0), (55, 80, 38, 16, -4, 4), (132, 215, 88, 42, -8, 8),
         (70, 60, 55, 30, 3, 4), (0, 0, 18, 38, 8, 2), (-95, -150, 62, 58, 12, -2), (-150, -235, 92, 75, 9, -4), (0, 0, 0, 0, 0, 0)]
    names = ['address', 'takeaway', 'top', 'transition', 'impact', 'release', 'finish']
    DUR = 6
    ox = 210

    def pose(k):
        a, c, sh, hp, lean, kn = k
        P = (ox + lean * .6, 290); S = (ox + lean, 205)
        sw = 40 * math.cos(math.radians(sh)) + 5; hw = 24 * math.cos(math.radians(hp)) + 5
        Ls, Rs = (S[0] - sw, S[1] + 4), (S[0] + sw, S[1] + 4)
        Lh, Rh = (P[0] - hw, P[1]), (P[0] + hw, P[1])
        ar = math.radians(a); hand = (S[0] + 74 * math.sin(ar), S[1] + 6 + 74 * math.cos(ar))
        cr = math.radians(c); club = (hand[0] + 76 * math.sin(cr), hand[1] + 76 * math.cos(cr))
        def elbow(s_, side):
            mx, my = (s_[0] + hand[0]) / 2, (s_[1] + hand[1]) / 2
            dx, dy = hand[0] - s_[0], hand[1] - s_[1]; n = math.hypot(dx, dy) or 1
            return mx - dy / n * 5 * side, my + dx / n * 5 * side
        return dict(P=P, S=S, Ls=Ls, Rs=Rs, Lh=Lh, Rh=Rh, hand=hand, club=club, Le=elbow(Ls, -1), Re=elbow(Rs, 1),
                    Lk=(Lh[0] - 7 - kn, 345), Rk=(Rh[0] + 7 + kn, 345), La=(Lh[0] - 13, 400), Ra=(Rh[0] + 13, 400),
                    head=(S[0] + lean * .3, S[1] - 34))
    poses = [pose(k) for k in K]
    bones = [('S', 'P'), ('Ls', 'Rs'), ('Lh', 'Rh'), ('Ls', 'Le'), ('Le', 'hand'), ('Rs', 'Re'), ('Re', 'hand'),
             ('Lh', 'Lk'), ('Lk', 'La'), ('Rh', 'Rk'), ('Rk', 'Ra'), ('S', 'head')]
    kt = ';'.join(f(i / (len(K) - 1)) for i in range(len(K)))
    ks = ';'.join(['.42 0 .58 1'] * (len(K) - 1))

    def lerp(t):
        n = len(K) - 1; i = min(int(t * n), n - 1); u = t * n - i; u = u * u * (3 - 2 * u)
        return tuple(K[i][j] + (K[i + 1][j] - K[i][j]) * u for j in range(6))
    b = f'<text x="0" y="22" class="caps">A · RECONSTRUCTED SKELETON</text><line x1="0" y1="34" x2="420" y2="34" stroke="{T["hair"]}"/>'
    b += f'<text x="500" y="22" class="caps">B · SEGMENT ROTATION ABOUT THE VERTICAL AXIS</text><line x1="500" y1="34" x2="1200" y2="34" stroke="{T["hair"]}"/>'
    b += f'<line x1="40" y1="403" x2="380" y2="403" stroke="{T["hair"]}"/>'
    for p in poses[1:-1]:
        for a_, z in bones + [('hand', 'club')]:
            b += f'<line x1="{f(p[a_][0])}" y1="{f(p[a_][1])}" x2="{f(p[z][0])}" y2="{f(p[z][1])}" stroke="{T["ink"]}" stroke-opacity=".08" stroke-width="1.2"/>'
    tr = [pose(lerp(i / 240))['club'] for i in range(241)]
    b += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in tr)}" fill="none" stroke="{T["acc"]}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="1.5 3.5"/>'
    for a_, z in bones + [('hand', 'club')]:
        an = ''
        for att, key, idx in (('x1', a_, 0), ('y1', a_, 1), ('x2', z, 0), ('y2', z, 1)):
            an += f'<animate attributeName="{att}" values="{";".join(f(p[key][idx]) for p in poses)}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/>'
        col = T['acc'] if z == 'club' else T['ink']
        b += f'<line x1="{f(poses[0][a_][0])}" y1="{f(poses[0][a_][1])}" x2="{f(poses[0][z][0])}" y2="{f(poses[0][z][1])}" stroke="{col}" stroke-width="{1.4 if z == "club" else 2}" stroke-linecap="round">{an}</line>'
    for key in ('head', 'S', 'Ls', 'Rs', 'Le', 'Re', 'hand', 'P', 'Lh', 'Rh', 'Lk', 'Rk', 'La', 'Ra'):
        vx = ';'.join(f(p[key][0]) for p in poses); vy = ';'.join(f(p[key][1]) for p in poses)
        if key == 'head':
            b += f'<circle r="10" fill="none" stroke="{T["ink"]}" stroke-width="2" cx="{vx.split(";")[0]}" cy="{vy.split(";")[0]}">'
        else:
            b += f'<circle r="2.6" fill="{T["ink"]}" cx="{vx.split(";")[0]}" cy="{vy.split(";")[0]}">'
        b += (f'<animate attributeName="cx" values="{vx}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{vy}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    b += f'<circle cx="{ox}" cy="399" r="3" fill="{T["ink"]}"/>'
    # plot
    px0, px1, py0, py1 = 540, 1080, 70, 390
    for v in (0, 30, 60, 90):
        y = py1 - v / 100 * (py1 - py0)
        b += f'<line x1="{px0}" y1="{f(y)}" x2="{px1}" y2="{f(y)}" stroke="{T["hair"]}" stroke-width="{1 if v == 0 else .6}"/>'
        b += f'<text x="{px0-8}" y="{f(y+3.5)}" class="mono mute" font-size="12" text-anchor="end">{v}°</text>'
    for i, nm in enumerate(names):
        x = px0 + (px1 - px0) * i / (len(K) - 2)
        b += f'<line x1="{f(x)}" y1="{py1}" x2="{f(x)}" y2="{py1+5}" stroke="{T["mute"]}"/><text x="{f(x)}" y="{py1+20}" class="serif mute" font-size="13.5" font-style="italic" text-anchor="middle">{nm}</text>'
    series = [('thorax', 2, T['ink']), ('pelvis', 3, T['acc2']), ('X-factor', None, T['acc'])]
    for nm, idx, col in series:
        pts = []
        for s in range(241):
            t = s / 240 * 6 / 7; k = lerp(t); v = k[idx] if idx is not None else max(0, k[2] - k[3])
            pts.append((px0 + (px1 - px0) * t, py1 - v / 100 * (py1 - py0)))
        d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".18" stroke-width="1.6"/>'
        b += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.8" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000">'
              f'<animate attributeName="stroke-dashoffset" values="1000;0;0" keyTimes="0;.857;1" dur="{DUR}s" repeatCount="indefinite"/></path>')
        ly = pts[-1][1] if nm != 'X-factor' else pts[-1][1]
        # direct label at peak instead of a legend
        peak = min(pts, key=lambda q: q[1])
        b += f'<text x="{f(peak[0]+8)}" y="{f(peak[1]-6)}" class="serif" font-size="14.5" font-style="italic" fill="{col}">{nm}</text>'
    b += (f'<line x1="{px0}" y1="{py0-6}" x2="{px0}" y2="{py1}" stroke="{T["ink"]}" stroke-opacity=".5" stroke-width=".8">'
          f'<animate attributeName="x1" values="{px0};{px1};{px1}" keyTimes="0;.857;1" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="x2" values="{px0};{px1};{px1}" keyTimes="0;.857;1" dur="{DUR}s" repeatCount="indefinite"/></line>')
    b += caption(0, 478, 2, 'A golf swing, reconstructed.',
                 'Thorax and pelvis rotation from the kinematic chain; their difference, the X-factor, peaks at the top of the backswing.')
    save(f'biomech-{TN}.svg', svg(W, H, b))


def spectro(cols, rows, seed=3):
    rnd = random.Random(seed)
    syl = [(.14, .07, [7, 18, 27]), (.36, .06, [5, 14, 30]), (.52, .05, [6, 20, 28]), (.70, .08, [4, 12, 24])]
    M = []
    for c in range(cols):
        t = c / cols; col = []
        for r in range(rows):
            v = .04 + rnd.random() * .06
            for cen, wd, fs in syl:
                e = math.exp(-((t - cen) / wd) ** 2)
                for fi, fr in enumerate(fs):
                    v += e * (.9 - fi * .2) * math.exp(-((r - fr) / 2.2) ** 2)
            col.append(min(1, v))
        M.append(col)
    return M


def wake():
    W, H = 1200, 380
    b = ''
    DUR = 6
    heads = [(0, 'A · WAVEFORM'), (300, 'B · LOG-MEL, 40 BANDS'), (600, 'C · TC-RESNET'), (900, 'D · DECISION, EVERY 50 MS')]
    for x, t in heads:
        b += f'<text x="{x}" y="22" class="caps">{t}</text><line x1="{x}" y1="34" x2="{x+270}" y2="34" stroke="{T["hair"]}"/>'
    for i in range(3):
        x = 276 + i * 300
        b += f'<path d="M{x} 170 L{x+18} 170" stroke="{T["mute"]}" stroke-width="1.1" marker-end="url(#arr)"/>'
    # waveform
    x0, x1, cy = 0, 262, 170
    syl = [(.14, .07), (.36, .06), (.52, .05), (.70, .08)]
    def wf(seed):
        r = random.Random(seed); pts = []
        for i in range(221):
            t = i / 220
            e = sum(math.exp(-((t - c) / w) ** 2) for c, w in syl) * .95 + .04
            pts.append((x0 + (x1 - x0) * t, cy + (r.random() * 2 - 1) * 78 * e))
        return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    ws = [wf(s) for s in (1, 2, 3)]
    b += f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{T["hair"]}"/>'
    b += (f'<path d="{ws[0]}" fill="none" stroke="{T["ink"]}" stroke-width=".9" stroke-linejoin="round">'
          f'<animate attributeName="d" values="{ws[0]};{ws[1]};{ws[2]};{ws[0]}" dur="1.8s" repeatCount="indefinite"/></path>')
    for (c, _), lab in zip(syl, ['hey', 'ce', 're', 'bel']):
        b += f'<text x="{f(x0+(x1-x0)*c)}" y="{cy+104}" class="serif mute" font-size="14.5" font-style="italic" text-anchor="middle">{lab}</text>'
    b += f'<rect x="{x0}" y="{cy-90}" width="1" height="180" fill="{T["acc"]}"><animate attributeName="x" values="{x0};{x1}" dur="{DUR}s" repeatCount="indefinite"/></rect>'
    # spectrogram (single-hue sequential)
    cols, rows = 54, 40
    M = spectro(cols, rows)
    sx, sy, cw, rh = 300, 82, 4.8, 4.4
    sw = cols * cw
    cells = ''
    for c in range(cols):
        for r in range(rows):
            v = M[c][r]
            if v < .12:
                continue
            cells += f'<rect x="{f(c*cw)}" y="{f((rows-1-r)*rh)}" width="{f(cw+.25)}" height="{f(rh+.25)}" fill="{T["ink"]}" fill-opacity="{f(min(1, v)**1.3)}"/>'
    b += f'<clipPath id="spc"><rect x="{sx}" y="{sy}" width="262" height="{f(rows*rh)}"/></clipPath>'
    b += f'<g clip-path="url(#spc)"><g><g id="spg" transform="translate({sx} {sy})">{cells}</g><use xlink:href="#spg" x="{f(sw)}"/>'
    b += f'<animateTransform attributeName="transform" type="translate" values="0 0;{f(-sw)} 0" dur="{DUR*1.6}s" repeatCount="indefinite"/></g></g>'
    b += f'<rect x="{sx}" y="{sy}" width="262" height="{f(rows*rh)}" fill="none" stroke="{T["hair"]}"/>'
    b += f'<rect x="{sx+204}" y="{sy-3}" width="56" height="{f(rows*rh+6)}" fill="none" stroke="{T["acc"]}" stroke-width="1.2"/>'
    b += f'<text x="{sx+232}" y="{f(sy+rows*rh+18)}" class="mono" font-size="12" fill="{T["acc"]}" text-anchor="middle">1.5 s window</text>'
    b += f'<text x="{sx}" y="{f(sy+rows*rh+18)}" class="mono mute" font-size="12">time →</text>'
    # TC-ResNet
    bx, by = 604, 96
    layers = [(14, 150, 'conv'), (20, 128, 'res'), (20, 110, 'res'), (24, 90, 'res'), (8, 40, 'fc')]
    xx = bx
    for i, (w, h, lab) in enumerate(layers):
        yy = by + (150 - h) / 2
        b += f'<path d="M{xx} {f(yy)} l10 -8 l{w} 0 l0 {h} l-10 8" fill="none" stroke="{T["mute"]}" stroke-width=".8"/>'
        b += (f'<rect x="{xx}" y="{f(yy)}" width="{w}" height="{h}" fill="{T["faint"]}" stroke="{T["ink2"]}" stroke-width="1">'
              f'<animate attributeName="stroke" values="{T["ink2"]};{T["acc"]};{T["ink2"]};{T["ink2"]}" keyTimes="0;.1;.2;1" dur="2.4s" begin="{f(i*.2)}s" repeatCount="indefinite"/></rect>')
        b += f'<text x="{f(xx+w/2)}" y="{by+176}" class="mono mute" font-size="12" text-anchor="middle">{lab}</text>'
        xx += w + 28
    b += f'<text x="{xx+4}" y="{by+80}" class="serif" font-size="20" font-style="italic">σ</text>'
    b += f'<text x="{bx}" y="{by+204}" class="mono mute" font-size="12">40 ch × 150 frames → p(wake)</text>'
    # decision
    dx0, dx1, dy0, dy1 = 900, 1170, 70, 260
    thr = .85; yt = dy1 - thr * (dy1 - dy0)
    b += f'<line x1="{dx0}" y1="{dy1}" x2="{dx1}" y2="{dy1}" stroke="{T["hair"]}"/>'
    b += f'<line x1="{dx0}" y1="{f(yt)}" x2="{dx1}" y2="{f(yt)}" stroke="{T["acc"]}" stroke-dasharray="3 3" stroke-width="1"/>'
    b += f'<text x="{dx1}" y="{f(yt-6)}" class="serif" font-size="14.5" font-style="italic" fill="{T["acc"]}" text-anchor="end">θ = 0.85</text>'
    sc = [.04, .05, .03, .08, .06, .12, .09, .18, .31, .52, .78, .91, .96, .93, .64, .33, .14, .07, .05, .04]
    n = len(sc)
    pts = [(dx0 + 6 + (dx1 - dx0 - 12) * i / (n - 1), dy1 - s * (dy1 - dy0)) for i, s in enumerate(sc)]
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    b += f'<path d="{d}" fill="none" stroke="{T["ink"]}" stroke-opacity=".15" stroke-width="1.4"/>'
    b += (f'<path d="{d}" fill="none" stroke="{T["ink"]}" stroke-width="1.4" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000">'
          f'<animate attributeName="stroke-dashoffset" values="1000;0;0" keyTimes="0;.7;1" dur="{DUR}s" repeatCount="indefinite"/></path>')
    for i, ((x, y), s) in enumerate(zip(pts, sc)):
        hit = s > thr
        t = .7 * i / (n - 1)
        b += (f'<circle cx="{f(x)}" cy="{f(y)}" r="{3.2 if hit else 2}" fill="{T["acc"] if hit else T["ink"]}" opacity="0">'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(max(t-.001,0))};{f(t)};.97;1" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    tw = .7 * 12 / (n - 1)
    b += (f'<text x="{dx0}" y="{dy1+24}" class="serif" font-size="15" font-style="italic" fill="{T["acc"]}" opacity="0">two consecutive frames over θ: wake'
          f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(tw)};{f(tw+.02)};.97;1" dur="{DUR}s" repeatCount="indefinite"/></text>')
    # numbers
    stats = [('20k', 'parameters'), ('< 1M', 'MACs per decision'), ('50 ms', 'decision stride'), ('4 × 10⁻⁶', 'max |C − PyTorch|')]
    x = 0
    for v, l in stats:
        v = v.replace('<', '&lt;')
        b += f'<text x="{x}" y="348" class="serif" font-size="26">{v}</text><text x="{x}" y="368" class="mono mute" font-size="12.5">{l}</text>'
        x += 300
    b += caption(0, 420, 3, '“Hey Cerebel”, keyword spotting on a glasses frame.',
                 'A temporal ResNet over 40 mel bands; the C port that ships in firmware matches PyTorch to six decimal places.')
    save(f'wake-{TN}.svg', svg(W, H, b))


def results():
    W, H = 1200, 322
    b = ''
    data = [('0.80', (93.1, 53.5), (96.3, 20.3)), ('0.90', (89.1, 30.9), (92.4, 6.8)), ('0.95', None, (87.8, 2.3))]
    panels = [(0, 'A · DETECTION RATE (HIGHER IS BETTER)', 0, 80, 100, '%'), (620, 'B · FALSE ACCEPTS PER HOUR (LOWER IS BETTER)', 1, 0, 60, '')]
    for px, title, idx, vmin, vmax, unit in panels:
        b += f'<text x="{px}" y="22" class="caps">{title}</text><line x1="{px}" y1="34" x2="{px+580}" y2="34" stroke="{T["hair"]}"/>'
        x0, y0, y1 = px + 44, 62, 262
        for g in range(5):
            v = vmin + (vmax - vmin) * g / 4; y = y1 - (y1 - y0) * g / 4
            b += f'<line x1="{x0}" y1="{f(y)}" x2="{px+580}" y2="{f(y)}" stroke="{T["hair"]}" stroke-width="{1 if g == 0 else .5}"/><text x="{x0-8}" y="{f(y+3.5)}" class="mono mute" font-size="12" text-anchor="end">{f(v)}{unit}</text>'
        for gi, (th, v1, v2) in enumerate(data):
            gx = x0 + 44 + gi * 170
            for bi, (val, col) in enumerate(((v1, T['mute']), (v2, T['acc']))):
                if val is None:
                    b += f'<text x="{gx+bi*40+15}" y="{y1-6}" class="mono mute" font-size="12" text-anchor="middle">—</text>'
                    continue
                vv = val[idx]; hgt = (y1 - y0) * (vv - vmin) / (vmax - vmin)
                b += f'<rect x="{gx+bi*40}" y="{f(y1-hgt)}" width="30" height="{f(hgt)}" fill="{col}" fill-opacity="{.35 if bi == 0 else .9}"/>'
                b += f'<text x="{gx+bi*40+15}" y="{f(y1-hgt-7)}" class="mono" font-size="13" fill="{col if bi else T["ink2"]}" text-anchor="middle">{vv}</text>'
            b += f'<text x="{gx+35}" y="{y1+20}" class="serif mute" font-size="14" font-style="italic" text-anchor="middle">θ = {th}</text>'
    b += f'<rect x="0" y="300" width="10" height="10" fill="{T["mute"]}" fill-opacity=".35"/><text x="16" y="309" class="serif ink2" font-size="14.5">v1, all voices (internal only)</text>'
    b += f'<rect x="210" y="300" width="10" height="10" fill="{T["acc"]}"/><text x="226" y="309" class="serif ink2" font-size="14.5">v2, commercial-safe voices only</text>'
    b += caption(0, 350, 4, 'v2 is better at every threshold.', 'Held-out speakers; 53 minutes of near-homophones and everyday dialogue.')
    save(f'results-{TN}.svg', svg(W, H, b))


def agents():
    W, H = 1200, 360
    b = ''
    N = {
        'in': (0, 168, 132, 50, 'Task', '“login page”'),
        'route': (172, 168, 128, 50, 'routeTask', 'intent router'),
        'boss': (342, 72, 136, 50, 'Director', 'Boss pipeline'),
        'arch': (520, 40, 124, 42, 'architect', None),
        'ui': (520, 106, 124, 42, 'ui-designer', None),
        'dev': (684, 73, 124, 42, 'developer', None),
        'qa': (848, 40, 110, 42, 'qa', None),
        'rev': (848, 106, 110, 42, 'reviewer', None),
        'coord': (342, 266, 136, 50, 'Coordinator', 'Multitask'),
        's1': (520, 236, 110, 34, 'stream 1', None),
        's2': (520, 274, 110, 34, 'stream 2', None),
        's3': (520, 312, 110, 34, 'stream n', None),
        'sdk': (684, 266, 164, 50, 'runWorkerViaSdk', '@cursor/sdk'),
        'bus': (1010, 168, 130, 50, 'EventBus', 'typed events', True),
    }
    for k, v in N.items():
        b += node(*v[:6], emph=len(v) > 6)
    def R(k): x, y, w, h = N[k][:4]; return x + w, y + h / 2
    def L(k): x, y, w, h = N[k][:4]; return x - 2, y + h / 2
    E = {}
    for a, z in [('in', 'route'), ('route', 'boss'), ('route', 'coord'), ('boss', 'arch'), ('boss', 'ui'), ('arch', 'dev'), ('ui', 'dev'),
                 ('dev', 'qa'), ('dev', 'rev'), ('qa', 'bus'), ('rev', 'bus'), ('coord', 's1'), ('coord', 's2'), ('coord', 's3'),
                 ('s1', 'sdk'), ('s2', 'sdk'), ('s3', 'sdk'), ('sdk', 'bus')]:
        pid = f'{a}_{z}'; E[pid] = curve(*R(a), *L(z))
        b += f'<path id="{pid}" d="{E[pid]}" fill="none" stroke="{T["mute"]}" stroke-width="1.1" marker-end="url(#arr)"/>'
    b += relay([(p, E[p]) for p in ('in_route', 'route_boss', 'boss_arch', 'arch_dev', 'dev_rev', 'rev_bus')], 6)
    b += relay([(p, E[p]) for p in ('route_coord', 'coord_s2', 's2_sdk', 'sdk_bus')], 6, T['acc2'], 2.8)
    for x, lab in ((520, 'stage 1, parallel'), (684, 'stage 2'), (848, 'stage 3, parallel')):
        b += f'<text x="{x}" y="22" class="serif mute" font-size="14" font-style="italic">{lab}</text>'
    b += f'<text x="1010" y="246" class="mono mute" font-size="12.5">→ Ink split panes</text><text x="1010" y="262" class="mono mute" font-size="12.5">→ tmux windows</text><text x="1010" y="278" class="mono mute" font-size="12.5">→ plain text</text>'
    b += caption(0, 410, 1, 'One prompt, many agents, one screen.',
                 'The Boss pipeline handles feature work; Multitask fans out across a repository. Both stream into one event bus.')
    save(f'agents-{TN}.svg', svg(W, H, b))


exec(open(__file__.replace('gen2.py', 'figs3d.py'), encoding='utf-8').read())
exec(open(__file__.replace('gen2.py', 'figs_body.py'), encoding='utf-8').read())
exec(open(__file__.replace('gen2.py', 'figs_real.py'), encoding='utf-8').read())
exec(open(__file__.replace('gen2.py', 'figs_system.py'), encoding='utf-8').read())
exec(open(__file__.replace('gen2.py', 'figs_recon2.py'), encoding='utf-8').read())
exec(open(__file__.replace('gen2.py', 'figs_tmodel.py'), encoding='utf-8').read())
for TN in ('light', 'dark'):
    T = THEMES[TN]
    header(); system(); biomech(); wake(); results(); agents(); golf3d(); tennis(); reconstruct(); glasses(); tmodel()
print('ok', sorted(os.listdir(OUT)))
