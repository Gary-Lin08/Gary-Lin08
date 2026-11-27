"""Pack one Tennis AI phase-1 session (TrackNet track + data contract) into JSON.

usage: python prep_tennis.py <phase1 dir> <session id> out.json
"""
import csv, json, sys

root, sid, out = sys.argv[1], sys.argv[2], sys.argv[3]
rd = lambda p: list(csv.DictReader(open(f'{root}/{p}', encoding='utf-8')))
track = rd(f'tracknet_tennis/outputs_v2/{sid}_tracknet_tennis.csv')
pay = json.load(open(f'{root}/data_contract/outputs/{sid}_v2_analysis_payload.json', encoding='utf-8'))['session']
rallies = rd(f'data_contract/outputs/{sid}_v2_rallies.csv')
shots = rd(f'data_contract/outputs/{sid}_v2_shots.csv')
bounces = rd(f'data_contract/outputs/{sid}_v2_bounces.csv')
num = lambda v: float(v) if v not in ('', None) else None
json.dump(dict(
    fps=pay['fps'], w=pay['width_px'], h=pay['height_px'], dur=pay['duration_sec'],
    court=[pay['court_width_m'], pay['court_length_m']],
    track=[[int(t['frame_num']), int(t['visible']), int(t['x']), int(t['y'])] for t in track],
    rallies=[dict(id=int(r['rally_id']), s=num(r['start_sec']), e=num(r['end_sec']), before=r['before_score'], after=r['after_score'], winner=r['winner_side']) for r in rallies],
    shots=[dict(f=int(s['frame_num']), t=num(s['time_sec']), x=num(s['x_px']), y=num(s['y_px']), xm=num(s['x_m']), ym=num(s['y_m']), side=s['hitter_side']) for s in shots],
    bounces=[dict(f=int(b['frame_num']), t=num(b['time_sec']), x=num(b['x_px']), y=num(b['y_px']), xm=num(b['x_m']), ym=num(b['y_m']), inside=b['in_court'] == '1') for b in bounces],
), open(out, 'w'))
print('ok', len(track), len(rallies), len(shots), len(bounces))
