"""Figure 8: Tennis AI model stack, drawn like an architecture figure in a paper.
All tensor sizes come from the repo's converters (GridTrackNet, MoveNet Lightning, stroke GRU)."""
import math


def tmodel():
    W, H = 1200, 470
    b = ''
    ink, mute, hair, acc, acc2, faint = T['ink'], T['mute'], T['hair'], T['acc'], T['acc2'], T['faint']
    DX, DY = .55, -.42      # oblique depth direction

    def cuboid(x, y, w, h, d, col, op=.16, lw=1):
        dx, dy = d * DX, d * DY
        s = f'<path d="M{f(x)} {f(y)} l{f(dx)} {f(dy)} h{f(w)} l{f(-dx)} {f(-dy)}z" fill="{col}" fill-opacity="{op*1.6}" stroke="{col}" stroke-width="{lw}" stroke-linejoin="round"/>'
        s += f'<path d="M{f(x+w)} {f(y)} l{f(dx)} {f(dy)} v{f(h)} l{f(-dx)} {f(-dy)}z" fill="{col}" fill-opacity="{op*2.4}" stroke="{col}" stroke-width="{lw}" stroke-linejoin="round"/>'
        s += f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="{lw}"/>'
        return s

    def label(x, y, t, cls='mono mute', size=11.5, anchor='middle', extra=''):
        return f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{size}" text-anchor="{anchor}"{extra}>{t}</text>'

    def stage(n, x, y, title):
        return (f'<circle cx="{x+9}" cy="{y-5}" r="9" fill="none" stroke="{acc}" stroke-width="1.2"/>'
                f'<text x="{x+9}" y="{y-1}" font-size="11.5" font-weight="700" fill="{acc}" text-anchor="middle">{n}</text>'
                f'<text x="{x+24}" y="{y}" class="serif" font-size="15.5" font-style="italic">{title}</text>')

    def flow(pid, d):
        return (f'<path id="{pid}" d="{d}" fill="none" stroke="{mute}" stroke-width="1.1" marker-end="url(#arr)"/>')

    # ---------------- row 1: ball branch
    r1 = 150
    b += stage('a', 0, 40, 'Ball: GridTrackNet')
    # input: 5 stacked frames
    for k in range(5):
        x0, y0 = 6 + k * 7, r1 - 40 - k * 6
        b += f'<rect x="{x0}" y="{y0}" width="96" height="56" fill="{faint}" stroke="{ink}" stroke-opacity="{.35 + .13*k}" stroke-width="1"/>'
        if k == 4:
            b += f'<path d="M{x0+18} {y0+48} L{x0+78} {y0+48} L{x0+66} {y0+16} L{x0+30} {y0+16}Z M{x0+48} {y0+16} L{x0+48} {y0+48}" fill="none" stroke="{mute}" stroke-width=".8"/>'
            b += f'<circle cx="{x0+60}" cy="{y0+26}" r="2.6" fill="{acc}"><animate attributeName="cx" values="{x0+36};{x0+70};{x0+36}" dur="3s" repeatCount="indefinite"/></circle>'
    b += label(66, r1 + 38, '5 frames × RGB') + label(66, r1 + 54, '432 × 768 × 15')
    # encoder cuboids (spatial sizes from 4 max-pool stages)
    sizes = [('432×768', 64, 86, 14), ('216×384', 52, 66, 22), ('108×192', 40, 50, 30), ('54×96', 30, 38, 38), ('27×48', 22, 28, 46)]
    x = 160
    centers = []
    for i, (lab, h, w, d) in enumerate(sizes):
        y = r1 - h / 2 + 4
        b += f'<g>{cuboid(x, y, w * .45, h, d, acc2 if i < 4 else acc, .12)}'
        b += (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w*.45)}" height="{h}" fill="none" stroke="{acc}" stroke-width="1.6" opacity="0">'
              f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.08;.2;1" dur="3s" begin="{f(i*.25)}s" repeatCount="indefinite"/></rect></g>')
        b += label(x + w * .22 + d * DX / 2, r1 + 56, lab)
        centers.append(x + w * .45 + d * DX)
        x = x + w * .45 + d * DX + 16
    b += label(160 + (x - 160) / 2 - 8, r1 + 74, 'conv + max-pool × 4', 'serif mute', 13.5, extra=' font-style="italic"')
    b += flow('t1', f'M118 {r1} L156 {r1}')
    # output grid 27 x 48 (conf, dx, dy) per frame
    gx, gy = x + 46, r1 - 40
    gw, gh = 96, 54
    b += flow('t2', f'M{f(x-6)} {r1} L{f(gx-4)} {r1}')
    for k in range(3):
        ox, oy = gx + k * 8, gy - k * 7
        b += f'<rect x="{ox}" y="{oy}" width="{gw}" height="{gh}" fill="{faint}" stroke="{ink}" stroke-opacity="{.35+.2*k}"/>'
    ox, oy = gx + 16, gy - 14
    for i in range(1, 12):
        b += f'<line x1="{f(ox+gw*i/12)}" y1="{oy}" x2="{f(ox+gw*i/12)}" y2="{oy+gh}" stroke="{hair}" stroke-width=".5"/>'
    for j in range(1, 7):
        b += f'<line x1="{ox}" y1="{f(oy+gh*j/7)}" x2="{ox+gw}" y2="{f(oy+gh*j/7)}" stroke="{hair}" stroke-width=".5"/>'
    cx_, cy_ = ox + gw * 7 / 12, oy + gh * 2 / 7
    b += f'<rect x="{f(cx_)}" y="{f(cy_)}" width="{f(gw/12)}" height="{f(gh/7)}" fill="{acc}"><animate attributeName="fill-opacity" values=".4;1;.4" dur="1.6s" repeatCount="indefinite"/></rect>'
    b += f'<path d="M{f(cx_+gw/24)} {f(cy_+gh/14)} l7 5" stroke="{ink}" stroke-width="1.2" marker-end="url(#arr)"/>'
    b += label(gx + 64, r1 + 38, '27 × 48 × 15') + label(gx + 64, r1 + 54, 'conf · Δx · Δy')
    # homography: image plane -> court plane
    hx = gx + 150
    b += stage('b', hx - 6, 40, 'Court homography')
    b += flow('t3', f'M{gx+gw+22} {r1} L{hx-2} {r1}')
    img = [(hx + 10, r1 + 26), (hx + 92, r1 + 26), (hx + 72, r1 - 22), (hx + 30, r1 - 22)]
    crt = [(hx + 118, r1 + 30), (hx + 196, r1 + 30), (hx + 196, r1 - 30), (hx + 118, r1 - 30)]
    b += f'<path d="M{" L".join(f"{a} {c}" for a, c in img)}Z" fill="{faint}" stroke="{ink}" stroke-width="1"/>'
    b += f'<path d="M{" L".join(f"{a} {c}" for a, c in crt)}Z" fill="{faint}" stroke="{ink}" stroke-width="1"/>'
    for (a1, c1), (a2, c2) in zip(img, crt):
        b += f'<line x1="{a1}" y1="{c1}" x2="{a2}" y2="{c2}" stroke="{acc2}" stroke-width=".8" stroke-dasharray="2 3"/><circle cx="{a1}" cy="{c1}" r="2.6" fill="{acc2}"/><circle cx="{a2}" cy="{c2}" r="2.6" fill="{acc2}"/>'
    b += f'<line x1="{hx+51}" y1="{r1+26}" x2="{hx+51}" y2="{r1-22}" stroke="{mute}" stroke-width=".7"/><line x1="{hx+157}" y1="{r1+30}" x2="{hx+157}" y2="{r1-30}" stroke="{mute}" stroke-width=".7"/>'
    b += label(hx + 104, r1 + 56, 'H ∈ ℝ³ˣ³ from 4 court keypoints') + label(hx + 104, r1 + 72, 'pixels → metres')
    # bounce
    bx = hx + 232
    b += stage('c', bx - 6, 40, 'Bounce')
    b += flow('t4', f'M{hx+202} {r1} L{bx-2} {r1}')
    b += f'<line x1="{bx}" y1="{r1+22}" x2="{bx+120}" y2="{r1+22}" stroke="{ink}" stroke-width="1"/>'
    pts = [(bx + i * 4, r1 + 22 - (40 * math.sin(math.pi * min(1, i / 18)) if i <= 18 else 22 * math.sin(math.pi * (i - 18) / 12))) for i in range(31)]
    b += f'<path id="bpath" d="M{" L".join(f"{f(x)} {f(y)}" for x, y in pts)}" fill="none" stroke="{acc}" stroke-width="1.4"/>'
    b += f'<circle r="3.4" fill="{acc}"><animateMotion dur="2.4s" repeatCount="indefinite"><mpath xlink:href="#bpath"/></animateMotion></circle>'
    b += f'<path d="M{bx+66} {r1+6} l6 10 l6 -10" fill="none" stroke="{ink}" stroke-width="1"/>'
    b += label(bx + 60, r1 + 56, 'sign flip of v_y') + label(bx + 60, r1 + 72, 'in / out from the court lines')

    # ---------------- row 2: stroke branch
    r2 = 345
    b += stage('d', 0, 250, 'Pose: MoveNet Lightning')
    b += f'<rect x="6" y="{r2-30}" width="80" height="60" fill="{faint}" stroke="{ink}" stroke-opacity=".6"/>'
    b += f'<circle cx="46" cy="{r2-16}" r="4" fill="none" stroke="{mute}"/><path d="M46 {r2-12} v14 M36 {r2-6} h20 M46 {r2+2} l-7 14 M46 {r2+2} l7 14" stroke="{mute}" fill="none"/>'
    b += label(6, r2 + 48, '192 × 192 × 3', anchor='start')
    b += flow('t5', f'M92 {r2} L124 {r2}')
    b += cuboid(130, r2 - 30, 28, 60, 22, acc2, .12) + cuboid(184, r2 - 20, 20, 40, 30, acc2, .12)
    b += label(172, r2 + 48, 'MobileNet') + label(172, r2 + 63, 'backbone')
    b += flow('t6', f'M228 {r2} L254 {r2}')
    kp = [(0, -22), (0, -14), (-8, -12), (8, -12), (-12, -2), (12, -2), (-13, 8), (13, 8), (-5, 6), (5, 6), (-6, 18), (6, 18), (-7, 28), (7, 28)]
    for (a1, c1) in kp:
        b += f'<circle cx="{270+a1}" cy="{r2-4+c1*.9}" r="2" fill="{acc2}"/>'
    b += f'<path d="M270 {r2-24} v20 M262 {r2-15} h16 M262 {r2-15} l-4 9 M278 {r2-15} l4 9 M265 {r2+1} l-1 10 l-1 10 M275 {r2+1} l1 10 l1 10" stroke="{acc2}" fill="none" stroke-width="1"/>'
    b += label(272, r2 + 48, '17 keypoints')
    # GRU unrolled
    b += stage('e', 320, 250, 'Stroke classifier: GRU')
    b += flow('t7', f'M292 {r2} L318 {r2}')
    gx0 = 330; cell = 46
    for i in range(7):
        x_ = gx0 + i * (cell + 18)
        if i == 5:
            b += label(x_ + cell / 2, r2 + 4, '⋯', 'serif', 20)
            continue
        b += f'<rect x="{x_}" y="{r2-18}" width="{cell}" height="36" rx="5" fill="{faint}" stroke="{ink}" stroke-opacity=".7"/>'
        b += label(x_ + cell / 2, r2 + 4, 'GRU', 'mono', 11.5)
        b += (f'<rect x="{x_}" y="{r2-18}" width="{cell}" height="36" rx="5" fill="{acc}" fill-opacity="0" stroke="none">'
              f'<animate attributeName="fill-opacity" values="0;.35;0;0" keyTimes="0;.1;.25;1" dur="3.5s" begin="{f(i*.35)}s" repeatCount="indefinite"/></rect>')
        b += f'<line x1="{x_+cell/2}" y1="{r2+48}" x2="{x_+cell/2}" y2="{r2+20}" stroke="{mute}" stroke-width=".9" marker-end="url(#arr)"/>'
        t_lab = 't = 30' if i == 6 else f't = {i+1}'
        b += label(x_ + cell / 2, r2 + 62, t_lab)
        if i < 6 and i != 4:
            b += f'<line x1="{x_+cell}" y1="{r2}" x2="{x_+cell+16}" y2="{r2}" stroke="{ink}" stroke-width="1" marker-end="url(#arr)"/>'
    b += label(gx0 + 3 * (cell + 18), r2 + 82, 'input 30 × 26 · pose features per frame')
    # dense + softmax
    sx = gx0 + 7 * (cell + 18) + 4
    b += flow('t8', f'M{sx-22} {r2} L{sx} {r2}')
    b += cuboid(sx + 4, r2 - 24, 10, 48, 10, acc2, .14) + cuboid(sx + 32, r2 - 16, 10, 32, 10, acc2, .14)
    b += label(sx + 30, r2 + 48, 'dense × 2')
    px = sx + 70
    b += flow('t9', f'M{sx+50} {r2} L{px-4} {r2}')
    classes = [('backhand', .06), ('forehand', .86), ('neutral', .05), ('serve', .03)]
    for i, (nm, p) in enumerate(classes):
        yy = r2 - 30 + i * 18
        b += f'<rect x="{px+62}" y="{yy-9}" width="70" height="11" fill="{faint}" stroke="{hair}"/>'
        b += (f'<rect x="{px+62}" y="{yy-9}" width="{f(70*p)}" height="11" fill="{acc if i == 1 else mute}" fill-opacity="{1 if i == 1 else .6}">'
              f'<animate attributeName="width" values="0;{f(70*p)};{f(70*p)}" keyTimes="0;.3;1" dur="3.5s" repeatCount="indefinite"/></rect>')
        b += label(px + 56, yy, nm, 'mono', 11.5, 'end')
    b += label(px + 70, r2 + 48, 'softmax over 4 classes')

    # ---------------- merge: state machine
    fx = 1050
    b += stage('f', fx - 20, 40, 'Rally + score')
    b += flow('t10', f'M{bx+128} {r1} C{fx-40} {r1} {fx-60} 210 {fx-6} 210')
    b += flow('t11', f'M{px+140} {r2} C{fx-40} {r2} {fx-60} 250 {fx-6} 250')
    states = [('serve', fx + 40, 130), ('rally', fx + 100, 200), ('point', fx + 40, 270), ('score', fx + 100, 340)]
    for nm, x_, y_ in states:
        b += f'<circle cx="{x_}" cy="{y_}" r="26" fill="{faint}" stroke="{ink}" stroke-opacity=".7"/>' + label(x_, y_ + 4, nm, 'serif', 13.5, extra=' font-style="italic"')
    arrows = [((fx + 40, 130), (fx + 100, 200)), ((fx + 100, 200), (fx + 40, 270)), ((fx + 40, 270), (fx + 100, 340)), ((fx + 100, 340), (fx + 40, 130))]
    for i, ((x1, y1), (x2, y2)) in enumerate(arrows):
        dxx, dyy = x2 - x1, y2 - y1; L_ = math.hypot(dxx, dyy); ux, uy = dxx / L_, dyy / L_
        a = (x1 + ux * 28, y1 + uy * 28); z = (x2 - ux * 30, y2 - uy * 30)
        bend = 18 if i < 3 else -60
        mx, my = (a[0] + z[0]) / 2 - uy * bend, (a[1] + z[1]) / 2 + ux * bend
        b += f'<path id="fs{i}" d="M{f(a[0])} {f(a[1])} Q{f(mx)} {f(my)} {f(z[0])} {f(z[1])}" fill="none" stroke="{mute}" stroke-width="1" marker-end="url(#arr)"/>'
    b += relay([(f'fs{i}', '') for i in range(4)], 6, acc, 3.2)
    b += relay([('t1', ''), ('t2', ''), ('t3', ''), ('t4', ''), ('t10', '')], 6, acc, 3)
    b += relay([('t5', ''), ('t6', ''), ('t7', ''), ('t8', ''), ('t9', ''), ('t11', '')], 6, acc2, 3)
    b += f'<text x="0" y="{H-12}" class="mono mute" font-size="12">tensor sizes from the shipped converters · a, d, e run on device as Core ML · b, c, f are geometry and state</text>'
    save(f'tmodel-{TN}.svg', svg(W, H, b))
