import sys, copy
sys.path.insert(0, '.')
from scen import *
GROUPS = {
 'inv/sync: collect_loop over all registry ids': ['rlk:player/inv/collect_loop'],
 'inv/sync: order_rebuild (held)': ['rlk:player/inv/order_rebuild_loop'],
 'inv/frame': ['rlk:player/inv/frame'],
 'inv/place_items': ['rlk:player/inv/place_items'],
 'inv/sweep_stray': ['rlk:player/inv/sweep_stray'],
 'equip_scan: scan_loop (all ids)': ['rlk:items/scan_loop'],
 '  of which scan_add_prep (held)': ['rlk:items/scan_add_prep'],
 'equip_scan: slate': ['rlk:items/slate/scan'],
 'engravings/scan: per-item loop': ['rlk:engravings/scan_loop'],
 'engravings/info_build: 12-pass sort': ['rlk:engravings/info_pass'],
 'engravings/info_build: groups+items': ['rlk:engravings/info_group_loop', 'rlk:engravings/info_gitem_loop', 'rlk:engravings/info_sum_loop', 'rlk:engravings/info_rest_sq', 'rlk:engravings/info_place'],
 'equip_scan: stat_light': ['rlk:items/stat_light'],
}
for tag, items, stars in (('small(3)', SMALL, 0), ('late(18,★★★)', LATE, 3)):
    s, pl = world(items, stars)
    c = pctx(s)
    snap = dict(s.incl); ml0 = copy.copy(s.macro_lines); mi0 = copy.copy(s.macro_n); a = s.n
    s.call('rlk:player/inv/manage', c); s.call('rlk:items/equip_scan', c)
    tot = s.n - a
    d = lambda f: s.incl[f] - snap.get(f, 0)
    # macro lines attributed to subtree: approximate by own fids under each group
    print(f'== {tag}: one dirty pass = {tot} commands; macro instantiations {sum(s.macro_n.values()) - sum(mi0.values())}, '
          f'macro lines substituted {sum(s.macro_lines.values()) - sum(ml0.values())}')
    for g, fs in GROUPS.items():
        print(f'   {g:45s} {sum(d(f) for f in fs):6d}')
    ml = {f: s.macro_lines[f] - ml0.get(f, 0) for f in s.macro_lines if s.macro_lines[f] - ml0.get(f, 0)}
    print('   macro lines by fid:', sorted(ml.items(), key=lambda x: -x[1])[:12])
