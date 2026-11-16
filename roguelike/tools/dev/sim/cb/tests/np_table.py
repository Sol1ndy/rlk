#!/usr/bin/env python3
"""np_table.py — the per-boss table of unparriable attacks from the hzlog.py logs (combat overhaul, fix lane FB).

    python3 np_table.py <log dir> <tag> [boss ...] [--md] [--json=<file>] [--cmp=<other tag>]

Reads <log dir>/<tag>_<boss>_{pat,dodge,fight}.json (hzlog.py `pat`, `pat --dodge`, `fight`). Per boss, pattern by pattern
(the pattern = the module folder that made the hazard: p/<name>, or the module's own group such as orb / fld / xt):

  hazards   the distinct shapes made (kind, reach, wind-up W, active A, damage %, per mille)
  state     P parryable · U unparriable and dodgeable · U-ND unparriable, no dodge (position only) · U-field unparriable
            lingering hazard (re-arming) — one letter per hazard, so a pattern can mix them
  glint     for U hazards: ticks from the warning glint to the strike (min-max over the pattern's hazards; the glint = the
            latest one >= 12 t before the strike, else the nearest earlier one); `none` = no glint in the 80 t before; for
            P / U-ND / U-field hazards a glint at their creation would be `!`
  avoid     with a perfect dodge on every tick (the --dodge log): how many of the pattern's hits were avoided / reached the judge
--cmp=<tag>: also the hazard and hit logs of the `fight` run of both tags compared (everything but NP / the glints).
"""
import json
import sys
from collections import OrderedDict
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OPT = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
ALL = ['guardian', 'butterfly', 'fieldgen', 'azhdaha', 'apep', 'tachy', 'arlecchino']
KIND = {1: 'disc', 2: 'ring', 3: 'sector', 4: 'line', 5: 'full', 6: 'mask'}
NAMES = {'guardian': '파수꾼・타락', 'butterfly': '달빛 환영 나비', 'fieldgen': '실험성 역장 발생 장치', 'azhdaha': '야타용왕',
         'apep': '아펩의 오아시스 파수꾼', 'tachy': '타키', 'arlecchino': '아를레키노'}
# pattern folder -> its name in the game (README boss sections, the modules' test/help)
PNAMES = {
    'guardian': {'p/thrust': 'P1 공간 찌르기', 'p/javelin': 'P2 공간 투창', 'p/slam': 'P3 공간을 집행하는 시련', 'p/pull': 'P4 어둠 속에서 퍼지는 공간',
                 'p/flyslam': 'P5 하늘을 심판하는 자', 'p/sweep_g': '파수 모드 휘두르기', 'p/sweep_e': '파수 모드 원소 휘두르기', 'p/fail': '파괴 실패 창'},
    'butterfly': {'p/kick': 'H1 달빛 발차기', 'p/jump': 'H2 달빛 점프', 'p/dash': 'H3 달빛 돌진', 'p/vacuum': 'H4 광폭한 진공', 'p/strike': 'B1 우아한 날개',
                  'p/barrage': 'B2 화염 날개의 습격', 'p/sweep': 'B3 날개 휩쓸개', 'p/coco': 'B4 달빛 축복', 'p/release': '달빛 해제'},
    'fieldgen': {'p/bomb': 'C1 일점 상쇄', 'p/slam': 'C2 내려찍기', 'p/laser': 'C3 코어 광선', 'p/missile': 'C4 바위 폭탄', 'p/burst': 'C5 지면 충격',
                 'p/rock': 'C6 파쇄', 'p/waves': '인력 충격파', 'p/fzone': 'F1 감소 영역', 'p/frock': 'F2 파쇄(역장)'},
    'azhdaha': {'p/chin': '턱 내려찍기', 'p/spikes': '가시', 'p/jump': '도약', 'p/burrow': '잠복', 'p/charge': '돌진', 'p/stomp': '발 구르기',
                'p/stomp3': '발 구르기(3)', 'p/feint': '성동격서', 'p/whip': '교활한 통수(꼬리 채찍)', 'p/tailslam': '꼬리 내려찍기', 'p/slide': '파멸의 산사태',
                'orb': '물 구체', 'fld': '불 장판', 'xt': '꼬리 원소 부가', 'xl': '다리 원소 부가', 'p/frost': '서리 습격(B3)', 'p/burrow3': 'B3 솟구침',
                'p/meteor': '운석', 'p/bolt': '벼락 습격(B3)', 'p/icicle': '고드름', 'p/shell': '물 포탄', 'p/icespike': '얼음 가시', 'p/elspike': '번개 가시'},
    'apep': {'p/burrow': 'P1 잠복 돌진', 'p/hands': 'P2 생명의 손', 'p/glow': 'P3 발광하는 파수꾼', 'p/wither': 'P4 초목이 시든 풍경', 'p/tail': 'P5 생명의 꼬리',
             'p/combo': 'P6 근접 콤보', 'p/mstrike': 'Q1 이동 돌진', 'p/aftermath': 'Q2 종말의 여파', 'p/shells': 'Q3 포탄', 'p/surface': 'Q3s 솟구침',
             'p/tail3': 'Q 꼬리(3단계)', 'p/spiral': 'Q5 나선'},
    'tachy': {'p/a1': '1 돌진 베기', 'p/b1': '2 날개 가리기 2연격', 'p/b2': '3 옆걸음 4연격', 'p/b3': '4 충전 6연격', 'p/c1': '5 연속기 · 블링크',
              'p/c2': '6 연속기 · 블링크 Ⅱ', 'p/c3': '7 붉은 핵 연속기', 'p/k': '8 블링크', 'p/w1': '9 지상 장풍', 'p/w2': '10 공중 장풍', 'p/l': '11 착지 공격',
              'p/mantle': '과부하 외피(깃털 · 노바)'},
    'arlecchino': {'p/a2': 'A 사형장으로의 초대 2타', 'p/a4': 'A 4타', 'p/a5': 'A 5타', 'p/b1': 'B 붉은 달의 낫', 'p/b2': 'B 손아귀', 'p/c1': 'C 불꽃 도약',
                   'p/c2': 'C 날개', 'p/d1': 'D 블러드 돌진', 'p/d2': 'D 추가타', 'p/e1': 'E 와리가리 베기', 'p/f1': 'F 붉은 피의 연회', 'p/g1': 'G 죽음의 칼날',
                   'p/h1': 'H 연옥 그림자 분신', 'p/q0': 'Q0 낙하 공격', 'p/q1': 'Q1 사형장으로의 초대(쌍낫)', 'p/q2': 'Q2 불꽃이 타오르는 낫',
                   'p/q3': 'Q3 붉은 죽음의 무도회', 'p/q4': 'Q4 떠오르는 재액의 달', 'p/q5a': 'Q5A 형벌의 핏값', 'p/q5b': 'Q5B 붉은 피의 사형', 'p/q6': 'Q6 핏빛 연회'},
}
HOW = {'P': 'parry (F) or perfect dodge', 'U': 'perfect dodge (no parry) - glint', 'U-ND': 'position / jump only (no parry, no dodge), own tell, no glint',
       'U-field': 'leave it (lingering; no parry), no glint'}
GLINT_BACK = 80
NP_LEAD = 12


def load(d, tag, boss, mode):
    p = Path(d) / f'{tag}_{boss}_{mode}.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None


def group_of(src):
    parts = src.split('/')
    parts = parts[2:] if parts[0] in ('mboss', 'boss') else parts
    if not parts:
        return '?'
    if parts[0] == 'p' and len(parts) > 1:
        return 'p/' + parts[1]
    return parts[0] if len(parts) < 3 or parts[0] not in ('wx', 'h', 'b') else '/'.join(parts[:2])


def state_of(h):
    if not h['NP']:
        return 'P'
    if h['ND']:
        return 'U-ND'
    if h['RA']:
        return 'U-field'
    return 'U'


def shape_of(h):
    k = KIND.get(h['K'], '?')
    r = f"{h['R'] / 1000:g}" if h['K'] not in (5, 6) else ''
    if h['K'] == 2:
        r = f"{h['R0'] / 1000:g}-{h['R'] / 1000:g}"
    if h['K'] == 6:
        r = f"safe {h['R0'] / 1000:g}"
    d = f"{h['PM']}‰" if h['PM'] else f"D{h['D']}"
    return f"{k} {r} {d}".replace('  ', ' ')


def glint_lead(h, glints):
    """Ticks from this hazard's warning glint to its strike: the latest glint that is at least NP_LEAD t before the strike
    (a glint nearer than that announces a later attack); when there is none, the nearest earlier glint (a late warning:
    the B-02 case); None without any glint in the GLINT_BACK ticks before."""
    s = h.get('strike')
    if s is None:
        return None
    g = [s - x['t'] for x in glints if s - GLINT_BACK <= x['t'] <= s]
    ok = [d for d in g if d >= NP_LEAD]
    return min(ok) if ok else (min(g) if g else None)


def rows_of(pat, dodge):
    """OrderedDict group -> dict(shapes, states, leads, hits, dodged, glint_bad)."""
    rows = OrderedDict()

    def row(g):
        return rows.setdefault(g, dict(shapes=OrderedDict(), st=OrderedDict(), leads=[], noglint=0, bad=0, hits=0, dodged=0,
                                       pj=0, pjU=0, dU=0, d=0, W=[]))
    for tid, v in (pat or {}).items():
        # (creation tick, maker) of the unparriable-and-dodgeable hazards: a glint made there is theirs
        u_made = {(h['t'], h['src']) for h in v['hz'] if (h['D'] or h['PM']) and state_of(h) == 'U'}
        for h in v['hz']:
            if not h['D'] and not h['PM']:
                continue                       # telegraph-only hazards
            r = row(group_of(h['src']))
            st = state_of(h)
            key = (shape_of(h), st)
            r['shapes'][key] = r['shapes'].get(key, 0) + 1
            r['st'][st] = r['st'].get(st, 0) + 1
            if st == 'U':
                r['W'].append(h['W'])
                ld = glint_lead(h, v['glint'])
                if ld is None:
                    r['noglint'] += 1
                else:
                    r['leads'].append(ld)
            elif (h['t'], h['src']) not in u_made and any(g['t'] == h['t'] and g['src'] == h['src'] for g in v['glint']):
                r['bad'] += 1                  # a glint made with a hazard that is not "unparriable: dodge it"
        for p in v['pj']:
            r = row(group_of(p['src']))
            r['pj'] += 1
            r['pjU'] += 1 if p['NP'] else 0
            st = 'U-ND' if p['NP'] and p['ND'] else 'U' if p['NP'] else 'P'
            r['st'][st] = r['st'].get(st, 0) + 1
        for d in v['direct']:
            r = row(group_of(d['src']))
            r['d'] += 1
            r['dU'] += 1 if d['NP'] else 0
    for tid, v in (dodge or {}).items():
        for h in v['hits']:
            g = group_of(h['src'])
            if g not in rows:                  # a prop's hit is logged under the function that moved it: no row of its own
                continue
            rows[g]['hits'] += 1
            rows[g]['dodged'] += h['dodged']
    return rows


def fmt_rows(rows):
    out = []
    for g, r in rows.items():
        shapes = '; '.join(f"{s} [{st}]" + (f" ×{n}" if n > 1 else '') for (s, st), n in r['shapes'].items())
        if r['pj']:
            shapes += ('; ' if shapes else '') + f"{r['pj']} projectile(s)" + (f" ({r['pjU']} U)" if r['pjU'] else '')
        if r['d']:
            shapes += ('; ' if shapes else '') + f"{r['d']} direct hit(s)" + (f" ({r['dU']} U)" if r['dU'] else '')
        st = ' + '.join(r['st'])
        if r['leads'] or r['noglint']:
            gl = (f"{min(r['leads'])}" + (f"-{max(r['leads'])}" if max(r['leads']) != min(r['leads']) else '') + ' t') if r['leads'] else ''
            if r['noglint']:
                gl += (' / ' if gl else '') + f"none ×{r['noglint']}"
        else:
            gl = '–'
        if r['bad']:
            gl += f" (! {r['bad']} glint(s) on a non-U hazard)"
        av = f"{r['dodged']}/{r['hits']}" if r['hits'] else '–'
        how = '; '.join(HOW[k] for k in ('P', 'U', 'U-ND', 'U-field') if k in r['st'])
        out.append((g, shapes, st, gl, av, how))
    return out


def counts(rows, fight):
    groups = len(rows)
    ug = sum(1 for r in rows.values() if any(s.startswith('U') for s in r['st']))
    ug_d = sum(1 for r in rows.values() if 'U' in r['st'])
    hz = [h for h in (fight or {}).get('hz', []) if h['D'] or h['PM']]
    return dict(groups=groups, with_u=ug, with_u_dodgeable=ug_d, fight_hz=len(hz), fight_np=sum(1 for h in hz if h['NP']),
                fight_u=sum(1 for h in hz if state_of(h) == 'U'), fight_glints=len((fight or {}).get('glint', [])),
                fight_hits=len((fight or {}).get('hits', [])),
                cmd=round(sum(fight['cmd']) / max(1, len(fight['cmd'])), 1) if fight else None)


def strip(fight):
    """The fight log without the parts the rule may change (NP, glints, commands)."""
    hz = [{k: v for k, v in h.items() if k not in ('NP',)} for h in fight['hz']]
    pj = [{k: v for k, v in p.items() if k not in ('NP',)} for p in fight['pj']]
    hits = [{k: v for k, v in h.items() if k not in ('NP',)} for h in fight['hits']]
    direct = [{k: v for k, v in h.items() if k not in ('NP',)} for h in fight['direct']]
    return dict(hz=hz, pj=pj, hits=hits, direct=direct, ticks=fight.get('ticks'))


def main():
    d, tag = ARGS[0], ARGS[1]
    bosses = ARGS[2:] or ALL
    res = {}
    for b in bosses:
        pat, dodge, fight = load(d, tag, b, 'pat'), load(d, tag, b, 'dodge'), load(d, tag, b, 'fight')
        if pat is None:
            continue
        rows = rows_of(pat, dodge)
        c = counts(rows, fight)
        res[b] = dict(rows=fmt_rows(rows), counts=c)
        print(f"\n### {NAMES.get(b, b)} ({b}) — {c['with_u']} of {c['groups']} attack groups have an unparriable part "
              f"({c['with_u_dodgeable']} dodgeable = with the glint)" + ('' if fight is None else
              f"; passive fight: {c['fight_np']} / {c['fight_hz']} hazards unparriable, {c['fight_glints']} glints, {c['fight_hits']} hits, "
              f"{c['cmd']} commands / tick"))
        print('| pattern | hazards [state] | glint → strike | avoided by | perfect dodge on every tick: avoided / hits |')
        print('|---|---|---|---|---|')
        for g, shapes, st, gl, av, how in res[b]['rows']:
            nm = PNAMES.get(b, {}).get(g)
            print(f'| {g}' + (f' {nm}' if nm else '') + f' | {shapes} | {gl} | {how} | {av} |')
        if 'cmp' in OPT and fight is not None:
            other = load(d, OPT['cmp'], b, 'fight')
            if other is not None:
                a, o = strip(fight), strip(other)
                same = {k: a[k] == o[k] for k in a}
                print(f"fight log vs {OPT['cmp']}: " + ', '.join(f"{k} {'same' if v else 'DIFFERENT'}" for k, v in same.items())
                      + f"; hazards {len(o['hz'])} -> {len(a['hz'])}, hits {len(o['hits'])} -> {len(a['hits'])}, HP lost "
                      f"{sum(h['lost'] for h in o['hits'])} -> {sum(h['lost'] for h in a['hits'])}, commands / tick "
                      f"{round(sum(other['cmd']) / len(other['cmd']), 1)} -> {c['cmd']}")
                res[b]['same'] = same
    if 'json' in OPT:
        Path(OPT['json']).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
