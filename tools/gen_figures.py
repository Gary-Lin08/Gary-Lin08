"""Generate animated SVG figures for Gary-Lin08's GitHub profile and repos."""
import math, os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono','Cascadia Code',Consolas,Menlo,monospace"
C = dict(bg0='#060A14', bg1='#0A1022', bg2='#101932', panel='#0D1530', line='#1E2A4D',
         text='#E8EEF9', mute='#93A1C0', dim='#56637F', cyan='#22D3EE', blue='#60A5FA',
         violet='#A78BFA', pink='#F472B6', amber='#FBBF24', green='#34D399', red='#FB7185')


def f(x):
    return f"{x:.1f}".rstrip('0').rstrip('.')


BASE_CSS = f"""
text{{font-family:{SANS};}}
.mono{{font-family:{MONO};}}
.t{{fill:{C['text']};}} .m{{fill:{C['mute']};}} .d{{fill:{C['dim']};}}
.flow{{stroke-dasharray:6 8;animation:flow 1.2s linear infinite;}}
.flowslow{{stroke-dasharray:3 9;animation:flow 2.4s linear infinite;}}
@keyframes flow{{to{{stroke-dashoffset:-28;}}}}
@keyframes up{{from{{opacity:0;transform:translateY(10px);}}to{{opacity:1;transform:none;}}}}
@keyframes fade{{from{{opacity:0;}}to{{opacity:1;}}}}
@keyframes pulse{{0%,100%{{opacity:.25;}}50%{{opacity:1;}}}}
@keyframes blink{{0%,49%{{opacity:1;}}50%,100%{{opacity:0;}}}}
"""


def frame(w, h, body, defs='', css='', fig=None, title=None, sub=None, grid=True):
    head = ''
    if fig:
        head += f'<text x="32" y="40" class="mono" font-size="12" fill="{C["cyan"]}" letter-spacing="2">{fig}</text>'
    if title:
        head += f'<text x="32" y="66" font-size="22" font-weight="650" class="t">{title}</text>'
    if sub:
        head += f'<text x="32" y="88" font-size="13.5" class="m">{sub}</text>'
    g = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#dots)" opacity=".55"/>' if grid else '')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
<style>{BASE_CSS}{css}</style>
<linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg1']}"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>
<radialGradient id="glowA" cx=".85" cy=".1" r=".7"><stop offset="0" stop-color="{C['violet']}" stop-opacity=".16"/><stop offset="1" stop-color="{C['violet']}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx=".05" cy=".95" r=".6"><stop offset="0" stop-color="{C['cyan']}" stop-opacity=".12"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{C['line']}"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
{defs}
</defs>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="url(#bgg)" stroke="{C['line']}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="url(#glowA)"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="url(#glowB)"/>
{g}
{head}
{body}
</svg>'''


def save(name, svg):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        fh.write(svg)
    print(name, len(svg) // 1024, 'KB')


def wave_path(x0, x1, cy, amp, k, phase, n=90, env=True):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        e = math.sin(math.pi * t) ** 1.5 if env else 1
        y = cy + amp * e * (math.sin(k * t * 2 * math.pi + phase) * .7 + .3 * math.sin(2.3 * k * t * 2 * math.pi + phase * 1.7))
        pts.append((x, y))
    return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)


def box(x, y, w, h, label, sub=None, color=C['cyan'], r=10, fs=13.5, anim_delay=None, mono_sub=True):
    s = f'<g>'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="{C["panel"]}" stroke="{color}" stroke-opacity=".55"/>'
    s += f'<rect x="{f(x)}" y="{f(y)}" width="3" height="{f(h)}" rx="1.5" fill="{color}" opacity=".9"/>'
    ty = y + h / 2 + (-3 if sub else 5)
    s += f'<text x="{f(x+14)}" y="{f(ty)}" font-size="{fs}" font-weight="600" class="t">{label}</text>'
    if sub:
        cls = 'mono' if mono_sub else ''
        s += f'<text x="{f(x+14)}" y="{f(ty+17)}" font-size="11" class="m {cls}">{sub}</text>'
    if anim_delay is not None:
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{r}" fill="none" stroke="{color}" stroke-width="1.6" style="animation:pulse 3s ease-in-out {anim_delay}s infinite"/>'
    return s + '</g>'


def packet(path_id, color, dur, begin, r=3.4):
    return (f'<circle r="{r}" fill="{color}" filter="url(#glow)" opacity="0">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath xlink:href="#{path_id}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')


def edge(pid, d, color, packets=(), width=1.6, cls='flow'):
    s = f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-opacity=".28" stroke-width="{width}"/>'
    s += f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity=".75" stroke-width="{width}" class="{cls}"/>'
    for (dur, begin) in packets:
        s += packet(pid, color, dur, begin)
    return s


def curve(x1, y1, x2, y2, bend=.5):
    dx = (x2 - x1) * bend
    return f'M{f(x1)} {f(y1)} C{f(x1+dx)} {f(y1)} {f(x2-dx)} {f(y2)} {f(x2)} {f(y2)}'


# ---------------------------------------------------------------- HERO
def hero():
    W, H = 1200, 380
    rnd = random.Random(7)
    body = ''
    # flowing signal waves
    cols = [C['cyan'], C['violet'], C['pink']]
    for i in range(3):
        ds = [wave_path(0, W, 300 + i * 12, 34 - i * 8, 2.2 + i * .7, ph + i) for ph in (0, 1.6, 3.2, 4.8)]
        vals = ';'.join(ds + [ds[0]])
        body += (f'<path d="{ds[0]}" fill="none" stroke="url(#wg)" stroke-width="{1.6 - i*.3}" opacity="{.55 - i*.12}">'
                 f'<animate attributeName="d" dur="{9 + i*2}s" repeatCount="indefinite" values="{vals}" calcMode="spline" keySplines="{";".join([".45 0 .55 1"]*4)}"/></path>')
    # constellation
    nodes = [(rnd.uniform(640, 1170), rnd.uniform(28, 350)) for _ in range(46)]
    links = ''
    for a in range(len(nodes)):
        for b in range(a + 1, len(nodes)):
            (x1, y1), (x2, y2) = nodes[a], nodes[b]
            dd = math.hypot(x1 - x2, y1 - y2)
            if dd < 92:
                links += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{C["blue"]}" stroke-opacity="{f(.28*(1-dd/92)+.04)}"/>'
    body += f'<g>{links}</g>'
    for i, (x, y) in enumerate(nodes):
        col = cols[i % 3]
        body += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rnd.uniform(1.3, 2.8))}" fill="{col}" style="animation:pulse {f(rnd.uniform(2.5,5))}s ease-in-out {f(rnd.uniform(0,4))}s infinite"/>'
    # rotating wireframe sphere
    cx, cy, R = 950, 180, 118
    sph = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sphg)" stroke="{C["cyan"]}" stroke-opacity=".45"/>'
    for lat in (-60, -30, 0, 30, 60):
        yy = cy - R * math.sin(math.radians(lat))
        rx = R * math.cos(math.radians(lat))
        sph += f'<ellipse cx="{cx}" cy="{f(yy)}" rx="{f(rx)}" ry="{f(rx*.18)}" fill="none" stroke="{C["violet"]}" stroke-opacity=".35"/>'
    steps = 36
    for m in range(8):
        base = m * math.pi / 8
        vals = ';'.join(f(abs(R * math.sin(base + 2 * math.pi * s / steps / 2))) for s in range(steps + 1))
        sph += (f'<ellipse cx="{cx}" cy="{cy}" rx="{f(abs(R*math.sin(base)))}" ry="{R}" fill="none" stroke="{C["cyan"]}" stroke-opacity=".38">'
                f'<animate attributeName="rx" dur="14s" repeatCount="indefinite" values="{vals}"/></ellipse>')
    # orbiting satellites
    sph += f'<ellipse id="orb1" cx="{cx}" cy="{cy}" rx="{R+38}" ry="{R*.32}" fill="none" stroke="{C["pink"]}" stroke-opacity=".35" stroke-dasharray="2 6" transform="rotate(-18 {cx} {cy})"/>'
    sph += f'<path id="orbp" d="M{cx-R-38} {cy} a{R+38} {f(R*.32)} 0 1 0 {2*(R+38)} 0 a{R+38} {f(R*.32)} 0 1 0 {-2*(R+38)} 0" fill="none" transform="rotate(-18 {cx} {cy})"/>'
    sph += f'<g transform="rotate(-18 {cx} {cy})"><circle r="4.5" fill="{C["pink"]}" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite"><mpath xlink:href="#orbp"/></animateMotion></circle>'
    sph += f'<circle r="3" fill="{C["amber"]}" filter="url(#glow)"><animateMotion dur="7s" begin="-3.5s" repeatCount="indefinite"><mpath xlink:href="#orbp"/></animateMotion></circle></g>'
    body += f'<g>{sph}</g>'
    # scan line
    body += f'<rect x="-120" y="0" width="120" height="{H}" fill="url(#scan)" opacity=".5"><animate attributeName="x" values="-120;{W}" dur="7s" repeatCount="indefinite"/></rect>'
    # text
    body += f'''
<g class="mono" font-size="13">
  <text x="64" y="86" fill="{C['cyan']}">~/gary-lin08 <tspan fill="{C['pink']}">❯</tspan> <tspan fill="{C['mute']}">perception · motion · agents</tspan></text>
  <rect x="404" y="75" width="8" height="14" fill="{C['cyan']}" style="animation:blink 1.1s step-end infinite"/>
</g>
<text x="62" y="164" font-size="70" font-weight="750" fill="url(#tg)" letter-spacing="-1.5">Gary Lin</text>
<text x="66" y="206" font-size="21" class="t" font-weight="500">On-device ML <tspan fill="{C['dim']}">·</tspan> 3D biomechanics <tspan fill="{C['dim']}">·</tspan> multi-agent tooling</text>
<text x="66" y="238" font-size="15.5" class="m">Building <tspan fill="{C['cyan']}" font-weight="600">Cerebel AI</tspan> — wearable perception that understands how people move.</text>
'''
    defs = f'''<linearGradient id="wg" x1="0" x2="1"><stop offset="0" stop-color="{C['cyan']}" stop-opacity="0"/><stop offset=".25" stop-color="{C['cyan']}"/><stop offset=".6" stop-color="{C['violet']}"/><stop offset=".9" stop-color="{C['pink']}"/><stop offset="1" stop-color="{C['pink']}" stop-opacity="0"/></linearGradient>
<linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#BFEFFF"/><stop offset="1" stop-color="{C['violet']}"/></linearGradient>
<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{C['cyan']}" stop-opacity="0"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity=".09"/></linearGradient>
<radialGradient id="sphg" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="{C['blue']}" stop-opacity=".22"/><stop offset="1" stop-color="{C['bg0']}" stop-opacity=".1"/></radialGradient>'''
    save('hero.svg', frame(W, H, body, defs))


# ---------------------------------------------------------------- CEREBEL STACK
def cerebel():
    W, H = 1200, 520
    b = ''
    lanes = [(32, 'EDGE · AR GLASSES', 'runs on the frame', C['cyan'], 330),
             (392, 'PHONE', 'bridge', C['violet'], 210),
             (632, 'CLOUD', 'reconstruction · reasoning', C['pink'], 536)]
    for x, name, sub, col, w in lanes:
        b += f'<rect x="{x}" y="112" width="{w}" height="352" rx="14" fill="{C["bg0"]}" fill-opacity=".55" stroke="{col}" stroke-opacity=".3" stroke-dasharray="4 5"/>'
        b += f'<text x="{x+16}" y="136" class="mono" font-size="11.5" fill="{col}" letter-spacing="1.5">{name}</text>'
        b += f'<text x="{x+w-16}" y="136" class="mono d" font-size="10.5" text-anchor="end">{sub}</text>'
    # nodes
    N = {
        'mic':   (52, 160, 130, 52, 'Mic · 16 kHz', 'log-mel 40×T', C['cyan']),
        'wake':  (200, 160, 146, 52, 'Wake word', 'TC-ResNet · C', C['cyan']),
        'cam':   (52, 300, 130, 52, 'Camera', 'egocentric RGB', C['pink']),
        'cap':   (200, 300, 146, 52, 'Capture', 'encode · stream', C['pink']),
        'app':   (412, 228, 170, 60, 'iPhone app', 'BLE / Wi-Fi relay', C['violet']),
        'pose':  (652, 160, 170, 54, '3D pose &amp; mesh', 'body-first recon', C['pink']),
        'ik':    (652, 300, 170, 54, 'Musculoskeletal IK', 'OpenSim model', C['amber']),
        'kin':   (850, 300, 150, 54, 'Kinematics', 'angles · loads', C['amber']),
        'kb':    (850, 160, 150, 54, 'Sport packs', 'RAG corpora', C['green']),
        'coach': (1026, 228, 124, 60, 'AI coach', 'LLM + tools', C['green']),
        'verify':(412, 380, 170, 50, 'Cloud re-verify', 'wake second pass', C['cyan']),
    }
    for i, (k, (x, y, w, h, l, s, col)) in enumerate(N.items()):
        b += box(x, y, w, h, l, s, col, anim_delay=i * .35)

    def R(k):
        x, y, w, h = N[k][:4]; return x + w, y + h / 2

    def L(k):
        x, y, w, h = N[k][:4]; return x, y + h / 2

    def T(k):
        x, y, w, h = N[k][:4]; return x + w / 2, y

    def B(k):
        x, y, w, h = N[k][:4]; return x + w / 2, y + h
    E = [('e1', curve(*R('mic'), *L('wake')), C['cyan'], [(1.4, 0)]),
         ('e2', curve(*R('wake'), *L('app')), C['cyan'], [(2.2, .3)]),
         ('e3', curve(*R('cam'), *L('cap')), C['pink'], [(1.4, .5)]),
         ('e4', curve(*R('cap'), *L('app')), C['pink'], [(2.2, .8), (2.2, 1.9)]),
         ('e5', curve(*R('app'), *L('pose')), C['pink'], [(2.4, 1.2), (2.4, 2.4)]),
         ('e6', f'M{f(T("ik")[0])} {f(B("pose")[1])} L{f(T("ik")[0])} {f(T("ik")[1])}', C['amber'], [(1.3, 1.5)]),
         ('e7', curve(*R('ik'), *L('kin')), C['amber'], [(1.2, 2)]),
         ('e8', curve(*R('kin'), *L('coach')), C['amber'], [(1.8, 2.3)]),
         ('e9', curve(*R('kb'), *L('coach')), C['green'], [(1.8, .7)]),
         ('e10', f'M{f(B("app")[0])} {f(B("app")[1])} L{f(T("verify")[0])} {f(T("verify")[1])}', C['cyan'], [(1.2, 1)]),
         ]
    for pid, d, col, pk in E:
        b += edge(pid, d, col, pk)
    # coach output bubble
    b += f'''<g style="animation:pulse 4s ease-in-out infinite">
<rect x="914" y="392" width="236" height="56" rx="12" fill="{C['panel']}" stroke="{C['green']}" stroke-opacity=".6"/>
<text x="928" y="414" class="mono" font-size="11" fill="{C['green']}">coach ▸</text>
<text x="928" y="434" font-size="12.5" class="t">"Lead knee at 162° at impact — stay flexed."</text></g>'''
    b += edge('e11', f'M1088 288 L1088 392', C['green'], [(1.4, 2.8)])
    # legend
    lg = [('audio', C['cyan']), ('video', C['pink']), ('kinematics', C['amber']), ('language', C['green'])]
    x = 32
    for name, col in lg:
        b += f'<circle cx="{x+6}" cy="490" r="4.5" fill="{col}" filter="url(#glow)"/><text x="{x+18}" y="494" class="mono m" font-size="11.5">{name}</text>'
        x += 120
    b += f'<text x="1160" y="494" class="mono d" font-size="11" text-anchor="end">every number the coach says comes from a deterministic tool, not the LLM</text>'
    save('cerebel-stack.svg', frame(W, H, b, fig='FIG. 1 — SYSTEM', title='Cerebel: from a glance to a coaching cue',
                                    sub='Wearable capture → on-device triggers → 3D musculoskeletal reconstruction → grounded AI coaching'))


# ---------------------------------------------------------------- BIOMECH (golf swing)
def biomech():
    W, H = 1200, 460
    # keyframes: (hand angle a, club angle c, thorax rot, pelvis rot, lean, knee)
    K = [(0, 0, 0, 0, 0, 0), (55, 80, 38, 16, -4, 4), (132, 215, 88, 42, -8, 8),
         (70, 60, 55, 30, 3, 4), (0, 0, 18, 38, 8, 2), (-95, -150, 62, 58, 12, -2), (-150, -235, 92, 75, 9, -4),
         (0, 0, 0, 0, 0, 0)]
    names = ['Address', 'Takeaway', 'Top', 'Transition', 'Impact', 'Release', 'Finish']
    DUR = 5.6
    ox, oy = 250, 0

    def pose(k):
        a, c, sh, hp, lean, kn = k
        P = (ox + lean * .6, 250)
        S = (ox + lean, 158)
        sw = 44 * math.cos(math.radians(sh)) + 6
        hw = 27 * math.cos(math.radians(hp)) + 6
        Ls, Rs = (S[0] - sw, S[1] + 4), (S[0] + sw, S[1] + 4)
        Lh, Rh = (P[0] - hw, P[1]), (P[0] + hw, P[1])
        ar = math.radians(a)
        hand = (S[0] + 112 * math.sin(ar), S[1] + 6 + 112 * math.cos(ar))
        cr = math.radians(c)
        club = (hand[0] + 112 * math.sin(cr), hand[1] + 112 * math.cos(cr))
        def elbow(sh_):
            mx, my = (sh_[0] + hand[0]) / 2, (sh_[1] + hand[1]) / 2
            dx, dy = hand[0] - sh_[0], hand[1] - sh_[1]
            n = math.hypot(dx, dy) or 1
            side = 1 if sh_ is Rs else -1
            return mx - dy / n * 6 * side, my + dx / n * 6 * side
        Le, Re = elbow(Ls), elbow(Rs)
        Lk, Rk = (Lh[0] - 8 - kn, 312), (Rh[0] + 8 + kn, 312)
        La, Ra = (Lh[0] - 14, 378), (Rh[0] + 14, 378)
        head = (S[0] + lean * .3, S[1] - 40)
        return dict(P=P, S=S, Ls=Ls, Rs=Rs, Lh=Lh, Rh=Rh, hand=hand, club=club, Le=Le, Re=Re, Lk=Lk, Rk=Rk, La=La, Ra=Ra, head=head)
    poses = [pose(k) for k in K]
    bones = [('S', 'P', C['text']), ('Ls', 'Rs', C['text']), ('Lh', 'Rh', C['text']), ('Ls', 'Le', C['cyan']), ('Le', 'hand', C['cyan']),
             ('Rs', 'Re', C['cyan']), ('Re', 'hand', C['cyan']), ('Lh', 'Lk', C['violet']), ('Lk', 'La', C['violet']),
             ('Rh', 'Rk', C['violet']), ('Rk', 'Ra', C['violet']), ('S', 'head', C['text']), ('hand', 'club', C['amber'])]
    kt = ';'.join(f(i / (len(K) - 1)) for i in range(len(K)))
    ks = ';'.join(['.42 0 .58 1'] * (len(K) - 1))
    b = ''
    # panel left
    b += f'<rect x="32" y="108" width="470" height="320" rx="14" fill="{C["bg0"]}" fill-opacity=".6" stroke="{C["line"]}"/>'
    b += f'<line x1="60" y1="380" x2="476" y2="380" stroke="{C["line"]}" stroke-width="2"/>'
    # onion skins
    for p in poses[1:-1]:
        for a_, b_, col in bones:
            b += f'<line x1="{f(p[a_][0])}" y1="{f(p[a_][1])}" x2="{f(p[b_][0])}" y2="{f(p[b_][1])}" stroke="{C["blue"]}" stroke-opacity=".07" stroke-width="2"/>'
    # club-head trajectory (dense sampled)
    def lerp_pose(t):
        n = len(K) - 1; i = min(int(t * n), n - 1); u = t * n - i
        u = u * u * (3 - 2 * u)
        return tuple(K[i][j] + (K[i + 1][j] - K[i][j]) * u for j in range(6))
    tr = [pose(lerp_pose(i / 240))['club'] for i in range(241)]
    trd = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in tr)
    b += f'<path d="{trd}" fill="none" stroke="url(#arc)" stroke-width="1.6" stroke-dasharray="2 5" opacity=".8"/>'
    # animated skeleton
    for a_, b_, col in bones:
        attrs = ''
        for att, key, idx in (('x1', a_, 0), ('y1', a_, 1), ('x2', b_, 0), ('y2', b_, 1)):
            vals = ';'.join(f(p[key][idx]) for p in poses)
            attrs += f'<animate attributeName="{att}" values="{vals}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/>'
        p0 = poses[0]
        w = 3.2 if col != C['amber'] else 2.2
        b += f'<line x1="{f(p0[a_][0])}" y1="{f(p0[a_][1])}" x2="{f(p0[b_][0])}" y2="{f(p0[b_][1])}" stroke="{col}" stroke-width="{w}" stroke-linecap="round">{attrs}</line>'
    for key in ('head', 'S', 'Ls', 'Rs', 'Le', 'Re', 'hand', 'P', 'Lh', 'Rh', 'Lk', 'Rk', 'La', 'Ra', 'club'):
        vx = ';'.join(f(p[key][0]) for p in poses); vy = ';'.join(f(p[key][1]) for p in poses)
        r = 11 if key == 'head' else (4.5 if key == 'club' else 3.6)
        fill = C['bg1'] if key == 'head' else (C['amber'] if key == 'club' else C['cyan'])
        stroke = f' stroke="{C["text"]}" stroke-width="2.4"' if key == 'head' else ''
        flt = '' if key == 'head' else ' filter="url(#glow)"'
        b += (f'<circle cx="{vx.split(";")[0]}" cy="{vy.split(";")[0]}" r="{r}" fill="{fill}"{stroke}{flt}>'
              f'<animate attributeName="cx" values="{vx}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{vy}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    b += f'<circle cx="{ox}" cy="376" r="4" fill="#fff"/>'
    b += f'<text x="52" y="132" class="mono" font-size="11" fill="{C["cyan"]}">markerless 2D/3D keypoints</text>'
    b += f'<text x="482" y="132" class="mono d" font-size="11" text-anchor="end">17 joints · 30 fps</text>'
    # phase label (switching)
    for i, nm in enumerate(names):
        t0 = i / (len(K) - 1); t1 = (i + 1) / (len(K) - 1)
        vals = '0;0;1;1;0;0' if i else '1;1;0;0'
        if i == 0:
            kts = f'0;{f(t1-.02)};{f(t1)};1'
        else:
            kts = f'0;{f(t0-.001)};{f(t0)};{f(t1-.02)};{f(t1)};1'
        b += (f'<text x="52" y="412" class="mono" font-size="13" fill="{C["amber"]}" opacity="{1 if i == 0 else 0}">▸ {nm.upper()}'
              f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" dur="{DUR}s" repeatCount="indefinite"/></text>')
    # right panel: plots
    px0, px1, py0, py1 = 590, 1150, 140, 380
    b += f'<rect x="530" y="108" width="638" height="320" rx="14" fill="{C["bg0"]}" fill-opacity=".6" stroke="{C["line"]}"/>'
    for v in (0, 30, 60, 90):
        y = py1 - (v / 100) * (py1 - py0)
        b += f'<line x1="{px0}" y1="{f(y)}" x2="{px1}" y2="{f(y)}" stroke="{C["line"]}" stroke-dasharray="2 4"/>'
        b += f'<text x="{px0-10}" y="{f(y+4)}" class="mono d" font-size="10.5" text-anchor="end">{v}°</text>'
    for i, nm in enumerate(names):
        x = px0 + (px1 - px0) * i / (len(K) - 1)
        b += f'<line x1="{f(x)}" y1="{py0}" x2="{f(x)}" y2="{py1}" stroke="{C["line"]}" stroke-opacity=".6"/>'
        b += f'<text x="{f(x)}" y="{py1+18}" class="mono d" font-size="10" text-anchor="middle">{nm}</text>'
    series = [('thorax rotation', 2, C['cyan']), ('pelvis rotation', 3, C['violet']), ('X-factor', None, C['pink'])]
    for j, (nm, idx, col) in enumerate(series):
        pts = []
        for s in range(241):
            t = s / 240; k = lerp_pose(t)
            v = k[idx] if idx is not None else max(0, k[2] - k[3])
            pts.append((px0 + (px1 - px0) * t, py1 - v / 100 * (py1 - py0)))
        d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".18" stroke-width="2"/>'
        b += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.4" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000" filter="url(#glow)">'
              f'<animate attributeName="stroke-dashoffset" values="1000;0" dur="{DUR}s" repeatCount="indefinite"/></path>')
        b += f'<circle cx="{px1+8-560}" cy="{124}" r="0"/>'
        lx = 600 + j * 170
        b += f'<rect x="{lx}" y="120" width="14" height="3" rx="1.5" fill="{col}"/><text x="{lx+20}" y="125" class="mono m" font-size="11">{nm}</text>'
    b += (f'<line x1="{px0}" y1="{py0}" x2="{px0}" y2="{py1}" stroke="#fff" stroke-opacity=".55">'
          f'<animate attributeName="x1" values="{px0};{px1}" dur="{DUR}s" repeatCount="indefinite"/><animate attributeName="x2" values="{px0};{px1}" dur="{DUR}s" repeatCount="indefinite"/></line>')
    defs = f'<linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="{C["amber"]}"/><stop offset="1" stop-color="{C["pink"]}"/></linearGradient>'
    save('biomech.svg', frame(W, H, b, defs, fig='FIG. 2 — BIOMECHANICS', title='Video → skeleton → joint kinematics',
                              sub='A swing reconstructed frame by frame; trunk–pelvis separation (X-factor) emerges from the kinematic chain'))


# ---------------------------------------------------------------- WAKE PIPELINE
def spectro_vals(cols, rows, seed=3):
    rnd = random.Random(seed)
    # syllables: hey / ce / re / bel — centered positions & formants
    syl = [(.14, .07, [7, 18, 27]), (.36, .06, [5, 14, 30]), (.52, .05, [6, 20, 28]), (.70, .08, [4, 12, 24])]
    M = []
    for c in range(cols):
        t = c / cols
        col = []
        for r in range(rows):
            v = .08 + rnd.random() * .07
            for (cen, wd, fs) in syl:
                e = math.exp(-((t - cen) / wd) ** 2)
                for fi, fr in enumerate(fs):
                    v += e * (.9 - fi * .2) * math.exp(-((r - fr) / 2.2) ** 2)
                if r < 3:
                    v += e * .3
            col.append(min(1, v))
        M.append(col)
    return M


def cmap(v):
    stops = [(0, (8, 12, 30)), (.25, (60, 30, 110)), (.5, (167, 70, 160)), (.75, (244, 114, 120)), (1, (251, 220, 120))]
    for i in range(len(stops) - 1):
        a, ca = stops[i]; b_, cb = stops[i + 1]
        if v <= b_:
            u = (v - a) / (b_ - a)
            return '#%02x%02x%02x' % tuple(int(ca[k] + (cb[k] - ca[k]) * u) for k in range(3))
    return '#fbdc78'


def wake_pipeline(name='wake-pipeline.svg'):
    W, H = 1200, 500
    b = ''
    DUR = 6
    panels = [(32, 'a', 'Raw audio', '16 kHz mono · 1.5 s window'),
              (322, 'b', 'Log-mel features', '40 bands · 25 ms / 10 ms hop'),
              (612, 'c', 'TC-ResNet', 'temporal convs · ~20k params'),
              (902, 'd', 'Decision', 'every 50 ms · 2-of-2 rule')]
    PW, PY, PH = 266, 116, 300
    for x, l, t, s in panels:
        b += f'<rect x="{x}" y="{PY}" width="{PW}" height="{PH}" rx="14" fill="{C["bg0"]}" fill-opacity=".6" stroke="{C["line"]}"/>'
        b += f'<text x="{x+16}" y="{PY+26}" class="mono" font-size="11" fill="{C["cyan"]}">({l})</text>'
        b += f'<text x="{x+42}" y="{PY+26}" font-size="14.5" font-weight="650" class="t">{t}</text>'
        b += f'<text x="{x+16}" y="{PY+46}" class="mono d" font-size="10.5">{s}</text>'
    for i in range(3):
        x = 32 + (i + 1) * 290 - 24
        b += edge(f'ar{i}', f'M{x-2} {PY+PH/2} L{x+22} {PY+PH/2}', C['cyan'], [(1, i * .3)])
        b += f'<path d="M{x+18} {PY+PH/2-5} l7 5 l-7 5" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/>'
    # (a) waveform
    rnd = random.Random(11)
    x0, x1, cy = 48, 282, 286
    syl = [(.14, .07), (.36, .06), (.52, .05), (.70, .08)]
    def wf(seed):
        r = random.Random(seed); pts = []
        for i in range(161):
            t = i / 160
            e = sum(math.exp(-((t - c) / w) ** 2) for c, w in syl) * .95 + .05
            pts.append((x0 + (x1 - x0) * t, cy + (r.random() * 2 - 1) * 78 * e))
        return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    ws = [wf(s) for s in (1, 2, 3)]
    b += f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{C["line"]}"/>'
    b += (f'<path d="{ws[0]}" fill="none" stroke="url(#wfg)" stroke-width="1.3" stroke-linejoin="round">'
          f'<animate attributeName="d" values="{ws[0]};{ws[1]};{ws[2]};{ws[0]}" dur="1.2s" repeatCount="indefinite"/></path>')
    for (cen, _), lab in zip(syl, ['hey', 'ce', 're', 'bel']):
        b += f'<text x="{f(x0+(x1-x0)*cen)}" y="{cy+102}" class="mono m" font-size="11" text-anchor="middle">{lab}</text>'
    b += (f'<rect x="{x0}" y="{cy-90}" width="2" height="180" fill="#fff" opacity=".7">'
          f'<animate attributeName="x" values="{x0};{x1}" dur="{DUR}s" repeatCount="indefinite"/></rect>')
    # (b) spectrogram scrolling
    cols, rows = 52, 40
    M = spectro_vals(cols, rows)
    sx, sy, cw, rh = 338, 186, 4.6, 4.6
    sw = cols * cw
    cells = ''
    for c in range(cols):
        for r in range(rows):
            cells += f'<rect x="{f(c*cw)}" y="{f((rows-1-r)*rh)}" width="{f(cw+.3)}" height="{f(rh+.3)}" fill="{cmap(M[c][r])}"/>'
    b += f'<clipPath id="spc"><rect x="{sx}" y="{sy}" width="{f(sw*0 + 234)}" height="{f(rows*rh)}" rx="6"/></clipPath>'
    b += f'<g clip-path="url(#spc)"><g><g id="spg" transform="translate({sx} {sy})">{cells}</g><use xlink:href="#spg" x="{f(sw)}"/>'
    b += f'<animateTransform attributeName="transform" type="translate" values="0 0;{f(-sw)} 0" dur="{DUR}s" repeatCount="indefinite"/></g></g>'
    b += f'<rect x="{sx}" y="{sy}" width="234" height="{f(rows*rh)}" rx="6" fill="none" stroke="{C["line"]}"/>'
    b += f'<text x="{sx}" y="{sy+rows*rh+20}" class="mono d" font-size="10">time →</text><text x="{sx+234}" y="{sy+rows*rh+20}" class="mono d" font-size="10" text-anchor="end">mel bin ↑</text>'
    b += (f'<rect x="{sx+180}" y="{sy-4}" width="50" height="{f(rows*rh+8)}" rx="4" fill="none" stroke="#fff" stroke-opacity=".8" stroke-dasharray="3 3"/>')
    b += f'<text x="{sx+205}" y="{sy-10}" class="mono" font-size="10" fill="#fff" text-anchor="middle">1.5 s</text>'
    # (c) TC-ResNet blocks
    bx, by = 640, 196
    layers = [(16, 150, C['blue'], 'conv 3×1'), (24, 128, C['violet'], 'res ×2'), (24, 108, C['violet'], 'res ×2'), (28, 86, C['pink'], 'res ×2'), (10, 40, C['amber'], 'GAP·FC')]
    xx = bx
    for i, (w, h, col, lab) in enumerate(layers):
        yy = by + (150 - h) / 2
        dx = 12
        b += f'<g style="animation:pulse 1.8s ease-in-out {f(i*.28)}s infinite">'
        b += f'<path d="M{xx} {f(yy)} l{dx} -10 l{w} 0 l0 {h} l-{dx} 10 z" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".7"/>'
        b += f'<rect x="{xx}" y="{f(yy)}" width="{w}" height="{h}" fill="{col}" fill-opacity=".35" stroke="{col}"/>'
        b += '</g>'
        b += f'<text x="{f(xx+w/2)}" y="{by+178}" class="mono m" font-size="9.5" text-anchor="middle">{lab}</text>'
        xx += w + 26
    # sigmoid out
    b += f'<circle cx="{xx+8}" cy="{by+75}" r="13" fill="none" stroke="{C["green"]}"/><text x="{xx+8}" y="{by+80}" font-size="14" text-anchor="middle" fill="{C["green"]}">σ</text>'
    b += f'<text x="{bx}" y="{PY+PH-24}" class="mono d" font-size="10">input 40 ch × 150 frames → p(wake)</text>'
    # (d) decision plot
    dx0, dx1, dy0, dy1 = 930, 1150, 190, 360
    thr = .85
    yt = dy1 - thr * (dy1 - dy0)
    b += f'<line x1="{dx0}" y1="{dy1}" x2="{dx1}" y2="{dy1}" stroke="{C["line"]}"/><line x1="{dx0}" y1="{dy0}" x2="{dx0}" y2="{dy1}" stroke="{C["line"]}"/>'
    b += f'<line x1="{dx0}" y1="{f(yt)}" x2="{dx1}" y2="{f(yt)}" stroke="{C["amber"]}" stroke-dasharray="4 4"/><text x="{dx1}" y="{f(yt-6)}" class="mono" font-size="10" fill="{C["amber"]}" text-anchor="end">θ = 0.85</text>'
    scores = [.04, .05, .03, .08, .06, .12, .09, .18, .31, .52, .78, .91, .96, .93, .64, .33, .14, .07, .05, .04]
    n = len(scores)
    pts = [(dx0 + 6 + (dx1 - dx0 - 12) * i / (n - 1), dy1 - s * (dy1 - dy0)) for i, s in enumerate(scores)]
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    b += (f'<path d="{d}" fill="none" stroke="{C["cyan"]}" stroke-width="2" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000">'
          f'<animate attributeName="stroke-dashoffset" values="1000;0;0" keyTimes="0;.7;1" dur="{DUR}s" repeatCount="indefinite"/></path>')
    for i, ((x, y), s) in enumerate(zip(pts, scores)):
        col = C['green'] if s > thr else C['cyan']
        t = .7 * i / (n - 1)
        b += (f'<circle cx="{f(x)}" cy="{f(y)}" r="{3.6 if s > thr else 2.4}" fill="{col}" opacity="0"{" filter=" + chr(34) + "url(#glow)" + chr(34) if s > thr else ""}>'
              f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(max(t-.001,0))};{f(t)};.97;1" dur="{DUR}s" repeatCount="indefinite"/></circle>')
    tw = .7 * 12 / (n - 1)
    b += (f'<g opacity="0"><rect x="{dx0+10}" y="{dy0-14}" width="128" height="26" rx="13" fill="{C["green"]}" fill-opacity=".15" stroke="{C["green"]}"/>'
          f'<text x="{dx0+74}" y="{dy0+3}" class="mono" font-size="11.5" fill="{C["green"]}" text-anchor="middle" font-weight="700">WAKE ✓ 2 / 2</text>'
          f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{f(tw)};{f(tw+.02)};.97;1" dur="{DUR}s" repeatCount="indefinite"/></g>')
    b += f'<text x="{dx0}" y="{dy1+20}" class="mono d" font-size="10">decisions @ 20 Hz →</text>'
    b += f'<text x="{dx0}" y="{PY+PH-14}" class="mono m" font-size="10.5">then: cloud re-verify ▸</text>'
    # stats strip
    stats = [('~20k', 'parameters'), ('&lt; 1M', 'MACs / decision'), ('50 ms', 'decision stride'), ('4×10⁻⁶', 'max |C − PyTorch|'), ('96.3%', 'recall @ θ 0.8, unseen speakers')]
    x = 32
    for v, l in stats:
        b += f'<text x="{x}" y="456" font-size="21" font-weight="700" fill="url(#sg)">{v}</text><text x="{x}" y="476" class="mono m" font-size="10.5">{l}</text>'
        x += 232
    defs = f'''<linearGradient id="wfg" x1="0" x2="1"><stop offset="0" stop-color="{C['cyan']}"/><stop offset="1" stop-color="{C['violet']}"/></linearGradient>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{C['cyan']}"/></linearGradient>'''
    save(name, frame(W, H, b, defs, fig='FIG. 3 — ALGORITHM', title='"Hey Cerebel" keyword spotting, end to end',
                     sub='A 20k-parameter temporal ResNet that fits in the glasses firmware and agrees with PyTorch to 6 decimals'))


# ---------------------------------------------------------------- WAKE RESULTS
def wake_results():
    W, H = 1200, 400
    b = ''
    data = {'0.80': ((93.1, 53.5), (96.3, 20.3)), '0.90': ((89.1, 30.9), (92.4, 6.8)), '0.95': (None, (87.8, 2.3))}
    panels = [(32, 'Detection rate', 'higher is better', 0, 100, '%', 80), (612, 'False accepts / hour', 'lower is better', 1, 60, '', 0)]
    for px, title, sub, idx, vmax, unit, vmin in panels:
        b += f'<rect x="{px}" y="108" width="556" height="262" rx="14" fill="{C["bg0"]}" fill-opacity=".6" stroke="{C["line"]}"/>'
        b += f'<text x="{px+20}" y="136" font-size="15" font-weight="650" class="t">{title}</text><text x="{px+536}" y="136" class="mono d" font-size="11" text-anchor="end">{sub}</text>'
        x0, y0, y1 = px + 60, 160, 330
        rng = vmax - vmin
        for g in range(5):
            v = vmin + rng * g / 4
            y = y1 - (y1 - y0) * g / 4
            b += f'<line x1="{x0}" y1="{f(y)}" x2="{px+530}" y2="{f(y)}" stroke="{C["line"]}" stroke-dasharray="2 4"/><text x="{x0-10}" y="{f(y+4)}" class="mono d" font-size="10.5" text-anchor="end">{f(v)}{unit}</text>'
        for gi, (th, (v1, v2)) in enumerate(data.items()):
            gx = x0 + 30 + gi * 156
            for bi, (val, col, lab) in enumerate(((v1, C['violet'], 'v1'), (v2, C['cyan'], 'v2'))):
                if val is None:
                    b += f'<text x="{gx+bi*52+22}" y="{y1-8}" class="mono d" font-size="10" text-anchor="middle">n/a</text>'
                    continue
                vv = val[idx]
                hgt = (y1 - y0) * (vv - vmin) / rng
                delay = gi * .25 + bi * .12
                b += (f'<rect x="{gx+bi*52}" y="{f(y1-hgt)}" width="44" height="{f(hgt)}" rx="5" fill="url(#bar{lab})">'
                      f'<animate attributeName="height" values="0;{f(hgt)};{f(hgt)}" keyTimes="0;.3;1" dur="6s" begin="{f(delay)}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1"/>'
                      f'<animate attributeName="y" values="{y1};{f(y1-hgt)};{f(y1-hgt)}" keyTimes="0;.3;1" dur="6s" begin="{f(delay)}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1"/></rect>')
                b += f'<text x="{gx+bi*52+22}" y="{f(y1-hgt-8)}" class="mono" font-size="11.5" fill="{col}" text-anchor="middle">{vv}</text>'
            b += f'<text x="{gx+48}" y="{y1+22}" class="mono m" font-size="11" text-anchor="middle">θ = {th}</text>'
    lx = 900
    for lab, col, txt in (('v1', C['violet'], 'v1 · all voices (internal)'), ('v2', C['cyan'], 'v2 · commercial-safe voices')):
        pass
    b += f'<rect x="760" y="60" width="12" height="12" rx="3" fill="{C["violet"]}"/><text x="778" y="70" class="mono m" font-size="11.5">v1 · all voices (internal only)</text>'
    b += f'<rect x="990" y="60" width="12" height="12" rx="3" fill="{C["cyan"]}"/><text x="1008" y="70" class="mono m" font-size="11.5">v2 · commercial-safe voices</text>'
    css = '@keyframes grow{from{transform:scaleY(0);}to{transform:scaleY(1);}}'
    defs = ''.join(f'<linearGradient id="bar{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="1" stop-color="{c}" stop-opacity=".25"/></linearGradient>' for k, c in (('v1', C['violet']), ('v2', C['cyan'])))
    save('wake-results.svg', frame(W, H, b, defs, css, fig='RESULTS — HELD-OUT SPEAKERS', title='v2 is better at every threshold',
                                   sub='53 min of hard negatives (near-homophones + everyday dialogue); speakers never seen in training'))


# ---------------------------------------------------------------- AGENT TEAM
def agent_arch(name='agent-arch.svg'):
    W, H = 1200, 560
    b = ''
    N = {
        'in':   (32, 236, 128, 56, 'Your task', '"add a login page"', C['text']),
        'route':(196, 236, 120, 56, 'routeTask', 'intent router', C['amber']),
        'boss': (360, 128, 130, 52, 'Director', 'Boss pipeline', C['cyan']),
        'arch': (530, 96, 118, 46, 'architect', None, C['cyan']),
        'ui':   (530, 168, 118, 46, 'ui-designer', None, C['cyan']),
        'dev':  (684, 132, 118, 46, 'developer', None, C['cyan']),
        'qa':   (838, 96, 104, 46, 'qa', None, C['cyan']),
        'rev':  (838, 168, 104, 46, 'reviewer', None, C['cyan']),
        'coord':(360, 352, 130, 52, 'Coordinator', 'Multitask', C['pink']),
        's1':   (530, 318, 104, 36, 'stream 1', None, C['pink']),
        's2':   (530, 362, 104, 36, 'stream 2', None, C['pink']),
        's3':   (530, 406, 104, 36, 'stream N', None, C['pink']),
        'sdk':  (684, 352, 150, 52, 'runWorkerViaSdk', '@cursor/sdk', C['violet']),
        'bus':  (978, 236, 120, 56, 'EventBus', 'typed events', C['green']),
    }
    for i, (k, (x, y, w, h, l, s, col)) in enumerate(N.items()):
        b += box(x, y, w, h, l, s, col, fs=13 if s else 12.5, anim_delay=i * .22)

    def R(k): x, y, w, h = N[k][:4]; return x + w, y + h / 2
    def L(k): x, y, w, h = N[k][:4]; return x, y + h / 2
    E = [('in', 'route', C['amber'], 0), ('route', 'boss', C['cyan'], .2), ('route', 'coord', C['pink'], .5),
         ('boss', 'arch', C['cyan'], .5), ('boss', 'ui', C['cyan'], .6), ('arch', 'dev', C['cyan'], 1), ('ui', 'dev', C['cyan'], 1.1),
         ('dev', 'qa', C['cyan'], 1.5), ('dev', 'rev', C['cyan'], 1.6), ('qa', 'bus', C['green'], 2), ('rev', 'bus', C['green'], 2.1),
         ('coord', 's1', C['pink'], .8), ('coord', 's2', C['pink'], .9), ('coord', 's3', C['pink'], 1),
         ('s1', 'sdk', C['violet'], 1.3), ('s2', 'sdk', C['violet'], 1.35), ('s3', 'sdk', C['violet'], 1.4), ('sdk', 'bus', C['green'], 1.8)]
    for i, (a, z, col, dl) in enumerate(E):
        b += edge(f'ag{i}', curve(*R(a), *L(z)), col, [(1.6, dl)])
    # stage brackets
    for x, lab in ((530, 'stage 1 · parallel'), (684, 'stage 2'), (838, 'stage 3 · parallel')):
        b += f'<text x="{x}" y="86" class="mono d" font-size="10.5">{lab}</text>'
    # UI outputs
    outs = [('Ink split-pane TUI', 150), ('tmux panes', 236), ('plain text', 322)]
    for lab, y in outs:
        pass
    # terminal mock to the right-bottom
    tx, ty = 878, 330
    b += f'<rect x="{tx}" y="{ty}" width="290" height="150" rx="10" fill="#05080F" stroke="{C["line"]}"/>'
    for i, col in enumerate((C['red'], C['amber'], C['green'])):
        b += f'<circle cx="{tx+16+i*14}" cy="{ty+14}" r="4" fill="{col}" opacity=".8"/>'
    b += f'<text x="{tx+278}" y="{ty+18}" class="mono d" font-size="10" text-anchor="end">ink · 4 panes</text>'
    pw, ph = 133, 54
    lines = [('architect', C['cyan']), ('ui-designer', C['cyan']), ('stream 1', C['pink']), ('stream 2', C['pink'])]
    for i, (lab, col) in enumerate(lines):
        x = tx + 8 + (i % 2) * (pw + 8); y = ty + 28 + (i // 2) * (ph + 6)
        b += f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="5" fill="none" stroke="{col}" stroke-opacity=".5"/>'
        b += f'<text x="{x+6}" y="{y+13}" class="mono" font-size="9.5" fill="{col}">{lab}</text>'
        for j in range(3):
            wfull = 40 + ((i * 37 + j * 23) % 70)
            b += (f'<rect x="{x+6}" y="{y+20+j*10}" width="{wfull}" height="4" rx="2" fill="{C["mute"]}" opacity=".55">'
                  f'<animate attributeName="width" values="0;{wfull};{wfull}" keyTimes="0;.4;1" dur="{2.4+i*.3}s" begin="{f(j*.35)}s" repeatCount="indefinite"/></rect>')
    b += edge('agb', f'M1038 292 L1038 330', C['green'], [(1, 2.4)])
    b = f'<g transform="translate(0 46)">{b}</g>'
    save(name, frame(W, H, b, fig='ARCHITECTURE', title='agent-team: one prompt, many agents, one screen',
                     sub='Boss pipeline for feature work, Multitask fan-out for repo-wide analysis — both stream into a shared event bus'))


# ---------------------------------------------------------------- PROJECT CARDS
def card(name, title, desc, tags, art, accent):
    W, H = 580, 200
    b = art
    b += f'<text x="28" y="44" class="mono" font-size="11" fill="{accent}" letter-spacing="1.5">{tags[0]}</text>'
    b += f'<text x="28" y="76" font-size="22" font-weight="700" class="t">{title}</text>'
    for i, line in enumerate(desc):
        b += f'<text x="28" y="{104+i*20}" font-size="13.5" class="m">{line}</text>'
    x = 28
    for t in tags[1:]:
        w = 9 + len(t) * 7.2
        b += f'<rect x="{x}" y="156" width="{f(w)}" height="22" rx="11" fill="{accent}" fill-opacity=".1" stroke="{accent}" stroke-opacity=".45"/><text x="{f(x+w/2)}" y="171" class="mono" font-size="11" fill="{accent}" text-anchor="middle">{t}</text>'
        x += w + 8
    save(name, frame(W, H, b, grid=False))


def cards():
    # wake card art: mini spectrum bars
    art = ''
    for i in range(22):
        x = 400 + i * 7.5
        h = 10 + 46 * abs(math.sin(i * .55)) * (0.5 + .5 * math.sin(i * .21 + 1))
        art += (f'<rect x="{f(x)}" y="{f(100-h/2)}" width="4.5" height="{f(h)}" rx="2" fill="url(#cg)">'
                f'<animate attributeName="height" values="{f(h)};{f(h*.35)};{f(h)}" dur="{f(.9+(i%5)*.17)}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="{f(100-h/2)};{f(100-h*.175)};{f(100-h/2)}" dur="{f(.9+(i%5)*.17)}s" repeatCount="indefinite"/></rect>')
    art += f'<defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["cyan"]}"/><stop offset="1" stop-color="{C["violet"]}"/></linearGradient></defs>'
    art += f'<text x="482" y="160" class="mono" font-size="10.5" fill="{C["green"]}" text-anchor="middle" style="animation:pulse 2s infinite">● listening</text>'
    card('card-wake.svg', 'Hey Cerebel', ['On-device wake word for AR glasses:', 'TC-ResNet in C, synthetic speech dataset.'],
         ['KEYWORD SPOTTING', 'PyTorch', 'C', 'TTS data'], art, C['cyan'])
    # agent card art: panes
    art = ''
    for i in range(4):
        x = 402 + (i % 2) * 78; y = 40 + (i // 2) * 64
        col = C['violet'] if i < 2 else C['pink']
        art += f'<rect x="{x}" y="{y}" width="70" height="56" rx="6" fill="#05080F" stroke="{col}" stroke-opacity=".6"/>'
        for j in range(3):
            w = 22 + (i * 13 + j * 17) % 36
            art += (f'<rect x="{x+7}" y="{y+12+j*13}" width="{w}" height="4" rx="2" fill="{col}" opacity=".7">'
                    f'<animate attributeName="width" values="0;{w};{w}" keyTimes="0;.5;1" dur="{2+i*.4}s" begin="{f(j*.3)}s" repeatCount="indefinite"/></rect>')
    card('card-agent.svg', 'agent-team-cli', ['Run a team of coding agents in parallel,', 'live in split panes. Cursor · Claude · Codex.'],
         ['MULTI-AGENT CLI', 'TypeScript', 'Ink', 'MCP'], art, C['violet'])
    # calculus card art: curve with sliding tangent
    art = ''
    X0, X1, Y0 = 392, 560, 120
    def fx(x): return Y0 - 38 * math.sin((x - X0) / 26) - (x - X0) * .05
    def dfx(x): return -38 * math.cos((x - X0) / 26) / 26 - .05
    pts = [(x, fx(x)) for x in range(X0, X1 + 1, 3)]
    art += f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in pts)}" fill="none" stroke="{C["amber"]}" stroke-width="2"/>'
    xs = list(range(X0 + 10, X1 - 9, 6)); xs = xs + xs[::-1]
    vcx = ';'.join(f(x) for x in xs); vcy = ';'.join(f(fx(x)) for x in xs)
    vx1 = ';'.join(f(x - 34) for x in xs); vx2 = ';'.join(f(x + 34) for x in xs)
    vy1 = ';'.join(f(fx(x) - 34 * dfx(x)) for x in xs); vy2 = ';'.join(f(fx(x) + 34 * dfx(x)) for x in xs)
    art += (f'<line stroke="{C["pink"]}" stroke-width="1.8"><animate attributeName="x1" values="{vx1}" dur="8s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="{vx2}" dur="8s" repeatCount="indefinite"/><animate attributeName="y1" values="{vy1}" dur="8s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{vy2}" dur="8s" repeatCount="indefinite"/></line>')
    art += (f'<circle r="4.5" fill="{C["pink"]}" filter="url(#glow)"><animate attributeName="cx" values="{vcx}" dur="8s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{vcy}" dur="8s" repeatCount="indefinite"/></circle>')
    art += f'<text x="476" y="176" class="mono" font-size="11" fill="{C["pink"]}" text-anchor="middle">f′(x) = slope of tangent</text>'
    card('card-calculus.svg', 'Calculus BC Quest', ['Browser game for AP Calculus BC practice:', 'pick a unit, a difficulty, and go.'],
         ['EDU GAME', 'HTML', 'Tailwind', 'GitHub Pages'], art, C['amber'])
    # tennis card art: ball trajectory with bounce
    art = ''
    def traj(t):  # t in 0..1 ; two arcs with bounce
        if t < .55:
            u = t / .55; x = 392 + 100 * u; y = 60 + 90 * u ** 2 if False else 50 + 4 * 95 * (u - .0) * (1 - u) * -1 + 95 * u
            return x, 50 + 100 * u - 60 * math.sin(math.pi * u)
        u = (t - .55) / .45; x = 492 + 72 * u
        return x, 150 - 70 * math.sin(math.pi * u)
    tp = [traj(i / 60) for i in range(61)]
    art += f'<line x1="388" y1="152" x2="568" y2="152" stroke="{C["green"]}" stroke-opacity=".5"/><line x1="470" y1="120" x2="470" y2="152" stroke="{C["mute"]}" stroke-opacity=".6" stroke-width="2"/>'
    art += f'<path id="tpath" d="M{" L".join(f"{f(x)} {f(y)}" for x, y in tp)}" fill="none" stroke="{C["green"]}" stroke-dasharray="2 5" opacity=".7"/>'
    art += f'<circle r="5" fill="#D9F99D" filter="url(#glow)"><animateMotion dur="2.6s" repeatCount="indefinite"><mpath xlink:href="#tpath"/></animateMotion></circle>'
    art += f'<circle cx="492" cy="150" r="3" fill="none" stroke="{C["amber"]}"><animate attributeName="r" values="2;12;2" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" dur="2.6s" repeatCount="indefinite"/></circle>'
    card('card-tennis.svg', 'Tennis AI', ['iOS tennis video analysis: ball tracking,', 'pose and shot recognition on device.'],
         ['SPORTS VISION', 'SwiftUI', 'Core ML', 'TrackNet'], art, C['green'])


def footer():
    W, H = 1200, 120
    b = ''
    ds = [wave_path(0, W, 60, 26, 3, ph, env=True) for ph in (0, 2, 4)]
    b += f'<path d="{ds[0]}" fill="none" stroke="url(#fw)" stroke-width="1.5"><animate attributeName="d" dur="8s" repeatCount="indefinite" values="{ds[0]};{ds[1]};{ds[2]};{ds[0]}"/></path>'
    b += f'<text x="600" y="66" class="mono m" font-size="12.5" text-anchor="middle" letter-spacing="3">THANKS FOR STOPPING BY</text>'
    defs = f'<linearGradient id="fw" x1="0" x2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset=".3" stop-color="{C["cyan"]}" stop-opacity=".6"/><stop offset=".7" stop-color="{C["pink"]}" stop-opacity=".6"/><stop offset="1" stop-color="{C["pink"]}" stop-opacity="0"/></linearGradient>'
    save('footer.svg', frame(W, H, b, defs, grid=False))


def banner(name, kicker, title, sub, accent):
    W, H = 1200, 260
    b = ''
    ds = [wave_path(640, W, 104, 40, 2.4, ph) for ph in (0, 2, 4)]
    for i in range(3):
        b += f'<path d="{ds[i]}" fill="none" stroke="{[C["cyan"],C["violet"],C["pink"]][i]}" stroke-opacity=".45" stroke-width="1.4"><animate attributeName="d" dur="{7+i}s" repeatCount="indefinite" values="{ds[i]};{ds[(i+1)%3]};{ds[(i+2)%3]};{ds[i]}"/></path>'
    b += f'<text x="56" y="84" class="mono" font-size="12.5" fill="{accent}" letter-spacing="2">{kicker}</text>'
    b += f'<text x="54" y="148" font-size="52" font-weight="750" fill="url(#tg2)" letter-spacing="-1">{title}</text>'
    b += f'<text x="57" y="190" font-size="17" class="m">{sub}</text>'
    defs = f'<linearGradient id="tg2" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{accent}"/></linearGradient>'
    save(name, frame(W, H, b, defs))


hero(); cerebel(); biomech(); wake_pipeline(); wake_results(); agent_arch(); cards(); footer()
banner('banner-wake.svg', 'CEREBEL AI · ON-DEVICE KEYWORD SPOTTING', 'Hey Cerebel', 'A wake word that runs inside AR glasses — model, training code, and a synthetic speech dataset.', C['cyan'])
banner('banner-agent.svg', 'MULTI-AGENT · TERMINAL UI', 'agent-team-cli', 'Run a team of coding agents in parallel and watch them work in split panes.', C['violet'])
banner('banner-calculus.svg', 'AP CALCULUS BC · BROWSER GAME', 'Calculus BC Quest', 'Pick a unit, pick a difficulty, and practice until it sticks.', C['amber'])
