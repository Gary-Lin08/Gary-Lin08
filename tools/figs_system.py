"""Isometric 'stack' version of the Cerebel system figure. Exec'd last; overrides system()."""
import math


def system():
    W, H = 1200, 500
    OX, OY, SX, SY, SZ, SK = 20, 70, 74, 50, 60, 36   # screen = OX + x*SX + y*SK, OY + y*SY - z*SZ
    P = lambda x, y, z=0: (OX + x * SX + y * SK, OY + y * SY - z * SZ)
    pt = lambda q: f'{f(q[0])} {f(q[1])}'
    def poly(pts, fill, stroke, sw=1, op=1, extra=''):
        return f'<path d="M{" L".join(pt(p) for p in pts)}Z" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'
    b = ''
    slabs = [(0, 3.6, 'EDGE · AR GLASSES', 'runs on the frame'), (4.4, 6.6, 'PHONE', 'BLE / Wi-Fi relay'), (7.4, 12.9, 'CLOUD', 'GPU reconstruction and reasoning')]
    for x0, x1, name, sub in slabs:
        y0, y1, t = 0, 4.2, .14
        top = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
        front = [P(x0, y1), P(x1, y1), P(x1, y1, -t), P(x0, y1, -t)]
        side = [P(x1, y0), P(x1, y1), P(x1, y1, -t), P(x1, y0, -t)]
        b += poly(front, T['hair'], T['hair'], .8, .6) + poly(side, T['hair'], T['hair'], .8, .35)
        b += poly(top, T['faint'], T['hair'], 1)
        for gx in [x0 + .5 * k for k in range(1, int((x1 - x0) / .5))]:
            a, c = P(gx, y0), P(gx, y1); b += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(c[0])}" y2="{f(c[1])}" stroke="{T["hair"]}" stroke-width=".4" stroke-opacity=".6"/>'
        lx, ly = P(x0, y1, -t)
        b += f'<text x="{f(lx)}" y="{f(ly+24)}" class="caps">{name}</text><text x="{f(lx)}" y="{f(ly+42)}" class="serif mute" font-size="13.5" font-style="italic">{sub}</text>'
    nodes = {
        'mic': (.4, .7, 'Microphone', '16 kHz audio', 'mic'), 'wake': (2.2, .7, 'Wake word', 'TC-ResNet in C', 'wave'),
        'cam': (.4, 2.8, 'Camera', 'egocentric RGB', 'cam'), 'cap': (2.2, 2.8, 'Capture', 'encode, stream', 'film'),
        'app': (5.0, 1.75, 'iPhone app', 'BLE / Wi-Fi', 'phone'),
        'pose': (7.8, .7, 'GEM-X', '3D body joints', 'body'), 'ik': (7.8, 2.8, 'OpenSim IK', 'musculoskeletal', 'bone'),
        'kin': (9.7, 2.8, 'Kinematics', 'angles, loads', 'graph'), 'kb': (9.7, .7, 'Sport packs', 'retrieval', 'book'),
        'coach': (11.6, 1.75, 'Coach', 'LLM + tools', 'chat'),
    }
    cw, cd, ch = .95, .75, .26
    def chip(x, y, label, sub, icon, emph=False):
        s = ''
        top = [P(x, y, ch), P(x + cw, y, ch), P(x + cw, y + cd, ch), P(x, y + cd, ch)]
        front = [P(x, y + cd, ch), P(x + cw, y + cd, ch), P(x + cw, y + cd), P(x, y + cd)]
        side = [P(x + cw, y, ch), P(x + cw, y + cd, ch), P(x + cw, y + cd), P(x + cw, y)]
        edge = T['acc'] if emph else T['ink2']
        s += poly(front, T['ink'], edge, .9, .10) + poly(side, T['ink'], edge, .9, .18)
        s += poly(top, T['faint'], edge, 1.1)
        cx = sum(p[0] for p in top) / 4; cy = sum(p[1] for p in top) / 4
        s += glyph(icon, cx, cy, T['acc'] if emph else T['ink'])
        tx, ty = P(x, y, ch)
        s += f'<text x="{f(tx-4)}" y="{f(ty-10)}" font-size="13.5" font-weight="600">{label}</text>'
        fx, fy = P(x, y + cd)
        s += f'<text x="{f(fx)}" y="{f(fy+16)}" class="mono mute" font-size="11">{sub}</text>'
        return s
    def glyph(kind, cx, cy, col):
        st = f'fill="none" stroke="{col}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"'
        if kind == 'mic':
            return f'<rect x="{f(cx-3)}" y="{f(cy-7)}" width="6" height="9" rx="3" {st}/><path d="M{f(cx-5.5)} {f(cy)} q5.5 6 11 0 M{f(cx)} {f(cy+3)} v3" {st}/>'
        if kind == 'wave':
            return f'<path d="M{f(cx-9)} {f(cy)} l3 0 l2 -5 l3 10 l3 -8 l2 3 l5 0" {st}/>'
        if kind == 'cam':
            return f'<rect x="{f(cx-8)}" y="{f(cy-5)}" width="16" height="10" rx="2" {st}/><circle cx="{f(cx)}" cy="{f(cy)}" r="3" {st}/>'
        if kind == 'film':
            return f'<rect x="{f(cx-8)}" y="{f(cy-5)}" width="16" height="10" rx="1" {st}/><path d="M{f(cx-2)} {f(cy-3)} l5 3 l-5 3z" {st}/>'
        if kind == 'phone':
            return f'<rect x="{f(cx-4)}" y="{f(cy-7)}" width="8" height="14" rx="2" {st}/><path d="M{f(cx-1.5)} {f(cy+4.5)} h3" {st}/>'
        if kind == 'body':
            return f'<circle cx="{f(cx)}" cy="{f(cy-6)}" r="2" {st}/><path d="M{f(cx)} {f(cy-4)} v6 M{f(cx-5)} {f(cy-2)} h10 M{f(cx)} {f(cy+2)} l-3 5 M{f(cx)} {f(cy+2)} l3 5" {st}/>'
        if kind == 'bone':
            return f'<path d="M{f(cx-6)} {f(cy-6)} l12 12" {st.replace('stroke-width="1.3"', 'stroke-width="2.2"')}/><circle cx="{f(cx-6)}" cy="{f(cy-6)}" r="2" {st}/><circle cx="{f(cx+6)}" cy="{f(cy+6)}" r="2" {st}/>'
        if kind == 'graph':
            return f'<path d="M{f(cx-8)} {f(cy+5)} l4 -4 l3 2 l4 -7 l5 4" {st}/>'
        if kind == 'book':
            return f'<path d="M{f(cx)} {f(cy-5)} q-4 -2 -8 0 v10 q4 -2 8 0 q4 -2 8 0 v-10 q-4 -2 -8 0 v10" {st}/>'
        if kind == 'chat':
            return f'<path d="M{f(cx-8)} {f(cy-6)} h16 v9 h-9 l-4 4 v-4 h-3z" {st}/>'
        return ''
    # connectors (drawn before chips so chips sit on top)
    def anchor(k, side):
        x, y = nodes[k][:2]
        if side == 'r': return (x + cw, y + cd / 2, .05)
        if side == 'l': return (x, y + cd / 2, .05)
        if side == 'b': return (x + cw / 2, y + cd, .05)
        if side == 't': return (x + cw / 2, y, .05)
    def bridge(a, c, lift=0.0, n=28):
        pts = []
        for i in range(n + 1):
            u = i / n
            x = a[0] + (c[0] - a[0]) * u; y = a[1] + (c[1] - a[1]) * (3 * u * u - 2 * u ** 3); z = a[2] + lift * 4 * u * (1 - u)
            pts.append(P(x, y, z))
        return 'M' + ' L'.join(pt(p) for p in pts)
    E = [('mic', 'r', 'wake', 'l', 0, 'a'), ('wake', 'r', 'app', 'l', .9, 'a'), ('cam', 'r', 'cap', 'l', 0, 'v'),
         ('cap', 'r', 'app', 'l', .9, 'v'), ('app', 'r', 'pose', 'l', 1.1, 'v'), ('pose', 'b', 'ik', 't', 0, 'v'),
         ('ik', 'r', 'kin', 'l', 0, 'v'), ('kin', 'r', 'coach', 'l', 0, 'v'), ('kb', 'r', 'coach', 'l', 0, 'k')]
    paths = {}
    for i, (a, sa, c, sc, lift, kind) in enumerate(E):
        d = bridge(anchor(a, sa), anchor(c, sc), lift)
        pid = f'sx{i}'; paths[pid] = (d, kind)
        col = {'a': T['acc2'], 'v': T['acc'], 'k': T['acc3']}[kind]
        b += f'<path id="{pid}" d="{d}" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="3.2" stroke-linecap="round"/>'
        b += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.2" stroke-dasharray="1 7" stroke-linecap="round"><animate attributeName="stroke-dashoffset" values="16;0" dur="1s" repeatCount="indefinite"/></path>'
    b += relay([(p, paths[p][0]) for p in ('sx2', 'sx3', 'sx4', 'sx5', 'sx6', 'sx7')], 7.5, T['acc'], 3.6)
    b += relay([(p, paths[p][0]) for p in ('sx0', 'sx1')], 4, T['acc2'], 3.2)
    for k, (x, y, lab, sub, ic) in nodes.items():
        b += chip(x, y, lab, sub, ic, emph=(k == 'coach'))
    # coach output as a pull-quote under the cloud slab
    qx, qy = P(7.4, 4.2, -.14); qx += 40
    qy += 70
    b += f'<line x1="{f(qx)}" y1="{f(qy-14)}" x2="{f(qx)}" y2="{f(qy+30)}" stroke="{T["acc"]}" stroke-width="2"/>'
    b += f'<text x="{f(qx+12)}" y="{f(qy+2)}" class="serif" font-size="17" font-style="italic">“Lead knee is at 162° at impact; stay flexed.”</text>'
    b += f'<text x="{f(qx+12)}" y="{f(qy+24)}" class="mono mute" font-size="12">the number comes from IK, not from the language model</text>'
    # legend
    lx, ly = 0, H - 22
    for i, (lab, col) in enumerate((('audio', T['acc2']), ('video and kinematics', T['acc']), ('retrieval', T['acc3']))):
        b += f'<line x1="{lx}" y1="{ly-4}" x2="{lx+22}" y2="{ly-4}" stroke="{col}" stroke-width="3" stroke-opacity=".6"/><text x="{lx+30}" y="{ly}" class="serif ink2" font-size="13.5">{lab}</text>'
        lx += 70 + len(lab) * 7
    save(f'system-{TN}.svg', svg(W, H, b))
