"""S2-B: P5 stomp, P5b triple stomp, P6 feint, P7 tail whip, P8 tail slam, P9 burrow charge (plan.md 5; s2.md 2.1).

Writes AZ:p/{stomp,stomp3,feint,whip,tailslam,burrow}/** only. Every hit is a framework hz/* (quiet, NoRx: the
g.hz_opts defaults); ticks, sizes and coefficient keys are plan.md 5 (binding), geometry from the rig manifest
(h_pb.py). The 10-20 telegraph rule (plan Change note 1) is applied row by row:
  keep  P9 rock rings (the chevron ring outline from the decision, tell 19)
  none  everything else: no kit decal; the readable tell is the clip pose + sound (paw lift, sways, tail raise) or a
        visible precursor (falling rocks, the dust mound / bulge at a breach, the mound and spires of the emergence);
        the impact preset plays at the hit tick.
Host side of the addon points (s2.md 10, 18.3): stomp/w1 + stomp/w3 (P5), stomp3/s1 + stomp3/s3 (P5b), whip/sweep +
whip/end (P7), tailslam/impact (P8), each called at E - 12 positioned / rotated as its context, the context scores set.
Pattern scratch: #aq<id><Name> (mb); entities: rlk_room rlk_mb_aux rlk_mb_az_pat rlk_mb_az_p<id> (+ m = markers /
props, h = hazards)."""
from . import api as A
from . import h_pb as HB
from .h_core import loc

L, K = A.L, A.K
DMG, KB = A.DMG, A.KB
PL = A.PLAYER
BODY = A.BODY
MK = 'minecraft:marker'

PATTERNS = [
    A.Pattern(5, 'stomp', '산명곡응', 'normal', {'by': 'paw', 'map': {1: 'stomp_fl', 2: 'stomp_fr', 3: 'stomp_hl', 4: 'stomp_hr'}},
              recover=18, max_len=80, length=63, weight={'head_near': 1, 'flank_near': 2, 'tail_off': 1, 'paw': 5},
              gates=('field_area',)),
    A.Pattern(10, 'stomp3', '산명곡응 – 연속 발구르기', 'normal', {'by': 'paw', 'map': {1: 'stomp3_fl', 2: 'stomp3_fr'}},
              phases=(3,), recover=20, max_len=100, length=85, replaces=5, gates=('field_area',)),
    A.Pattern(6, 'feint', '성동격서', 'normal', 'feint', recover=14, max_len=60, length=50),
    A.Pattern(7, 'whip', '교활한 통수', 'normal', {'by': 'side', 'map': {1: 'tail_whip_l', -1: 'tail_whip_r'}},
              recover=18, max_len=80, length=64, weight={'flank_far': 1, 'tail_off': 2}, gates=('anchor8', 'exit')),
    A.Pattern(8, 'tailslam', '꼬리찍기', 'normal', 'tail_slam', recover=18, max_len=85, length=70,
              weight={'tail_lane': 4, 'tail_off': 1}, gates=('anchor8', 'field_area')),
    A.Pattern(9, 'burrow', '잠복 돌진', 'normal', 'burrow_dive', phases=(1,), cooldown=600, recover=24, max_len=320,
              length=273, weight={'head_near': 1, 'head_mid': 2, 'head_far': 2, 'flank_far': 1, 'tail_lane': 1, 'tail_off': 1},
              hooks=('resume',)),
]


# =============================================================================================================== common
def tags(pid, kind):
    """Tags of an entity a pattern makes (s2.md 12): the room / aux / pattern tags + rlk_mb_az_p<id> + p<id><kind>."""
    return f'Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p{pid}","rlk_mb_az_p{pid}m","rlk_mb_az_p{pid}{kind}"]'


def marker(pid, kind, pos='~ ~ ~'):
    return f'summon {MK} {pos} {{{tags(pid, kind)}}}'


def hz(g, pid, call, *, el='ground', grp='cur', nd=None, low=None, kb=None, kbdir=None, act=None, extra=(), pos=None):
    """One framework hazard: options (quiet / NoRx from g.hz_opts), the element, the make call (wrapped in `pos`, an
    `execute ...` prefix, when given) and the tags rlk_mb_az_p<id> + p<id>h (+ extra)."""
    out = [g.GRP_NEW] if grp == 'new' else []
    out += g.hz_opts(grp=grp in ('new', 'cur'), nododge=nd, y1=low, kb=kb, kbdir=kbdir, act=act)
    if isinstance(grp, str) and grp.startswith('#'):      # a group saved in a score (made over several ticks)
        out.append(f'scoreboard players operation #hzGrp mb = {grp} mb')
    out += g.el_ground() if el == 'ground' else g.el_tail() if el == 'tail' else g.el(el)
    out.append(f'{pos} run {call}' if pos else call)
    out += [g.tag_last_hz(f'rlk_mb_az_p{pid}'), g.tag_last_hz(f'rlk_mb_az_p{pid}h')] + [g.tag_last_hz(t) for t in extra]
    return out


def keep_grp(name):
    return f'scoreboard players operation {name} mb = #mbGrp mb'


def addon_fn(g, key, name, point, scores, yaw_from_ctx=True):
    """p/<key>/<name>: the context scores, the context marker (g.addon's first line, at the caller's position /
    rotation), #azCtxYaw read from it, then the core dispatcher (s2.md 10.1). Returns the function line."""
    ad = A._flat(g.addon(point))
    assert len(ad) == 2, ad
    lines = [f'# addon point {point} (host side, called at E - 12 = {A.ADDON_POINTS[point]["call"]}; s2.md 10)'] + list(scores)
    lines.append(ad[0])
    if yaw_from_ctx:
        lines.append(f'execute store result score #azCtxYaw mb run data get entity @e[type={MK},tag=rlk_az_ctx,limit=1] Rotation[0]')
    lines.append(ad[1])
    g.pw(key, name, lines)
    return g.fn(f'p/{key}/{name}')


def cancel_lines(pid, extra=()):
    """Selectors only (any executor), idempotent: the pattern's live hazards end (hz/expire), its markers / props go."""
    return [f'# cancel P{pid}: its hazards (rlk_mb_az_p{pid}h) expire, its markers and props go',
            f'execute as @e[type={MK},tag=rlk_mb_hz,tag=rlk_mb_az_p{pid}h] at @s rotated as @s run function rlk:mboss/hz/expire',
            f'kill @e[tag=rlk_mb_az_p{pid}m]'] + list(extra)


def head(p, text):
    return [f'# {p.label} ({p.key}, id {p.id}) - {text}']


def P(pid):
    return next(p for p in PATTERNS if p.id == pid)


# ================================================================================================= P5 stomp (id 5)
def emit_stomp(g):
    p, c = P(5), HB.P5
    key, pid = p.key, p.id
    tl = A.TL(g, key)
    at_paw = f'execute at @e[type={MK},tag=rlk_mb_az_p5paw,limit=1] run '
    sub = HB.Sub(g, key, 'w')                      # runs at the paw marker
    start = head(p, 'start (#azPT 0; the core played stomp_<paw> by #azPaw)') + [
        'scoreboard players operation #aq5P mb = #azPaw mb',
        'execute unless score #aq5P mb matches 1..4 run scoreboard players set #aq5P mb 1',
        f'kill @e[tag=rlk_mb_az_p5m]']
    for n, clip in ((1, 'stomp_fl'), (2, 'stomp_fr'), (3, 'stomp_hl'), (4, 'stomp_hr')):
        s, f = HB.STOMP_PAW[clip]
        start.append(f'execute if score #aq5P mb matches {n} positioned {loc(s, f)} run {marker(pid, "paw", "~ 201 ~")}')
    # the three fronts (N10, tele 'none': the travelling front is the hazard's own visual; plan Change note 1)
    gvars = ('#aq5G1', '#aq5G2', '#aq5G3')
    for i, strike in enumerate(c['strikes']):
        made = strike - c['tell']
        g.wave(sub, strike, c['r0'], c['r1'], None, c['band'], c['tell'], DMG[c['dmg']], el='ground', grp='new',
               low=c['low'], ease=c['ease'], wid=c['wid'][i], tag=f'rlk_mb_az_p5w{i + 1}')
        sub.at(made, g.tag_last_hz('rlk_mb_az_p5'), g.tag_last_hz('rlk_mb_az_p5h'), keep_grp(gvars[i]))
        if i == 0:                                 # the slam disc r 2.8 at the paw, in w1's group
            sub.at(made, *hz(g, pid, L.hz_disc(c['slam_r'], c['tell'], DMG[c['dmg']]), grp='cur'))
        sub.at(strike, g.snd('stomp_wave'))
        if i == 0:                                 # the paw's crystal cluster + cracks at the slam's hit, dust at the others
            # (FIX STATE-2: the cracks spread 1 t after the impact; the contact tick also plays the slam sound + crown)
            sub.at(strike, g.fxe('impact', 'ground'))
            sub.at(strike + 1, g.fxe('cracks', 'ground', r=4.5))
        else:
            sub.at(strike, g.fxe('dust_ring', 'ground', r=c['slam_r']))
    # (FIX FID-1) the slam sound and the crown burst on the paw's contact = the w1 strike (the clip's slam event is the
    # downstroke start, 4 t before the paw meets the floor); (FIX FAIR-7) the lift sound 2 t before the clip's lift
    sub.at(c['strikes'][0], g.snd('stomp_slam'))
    sub.at(c['strikes'][0] + 1, g.fxe('crown', 'ground'))       # (FIX STATE-2) the crown rises 1 t after the contact
    sub.at(c['ev']['lift'] - LIFT_LEAD, g.sound('block.deepslate.step', 1.0, 0.6), g.sound('entity.ravager.step', 0.8, 0.5))
    # addon points: stomp/w1 (E 17, call 5; w1's group), stomp/w3 (E 47, call 35; w3's group)
    for point, grp_var in (('stomp/w1', '#aq5G1'), ('stomp/w3', '#aq5G3')):
        d = A.ADDON_POINTS[point]
        fn = addon_fn(g, key, 'ax_' + d['event'], point, [
            'scoreboard players operation #azCtxPaw mb = #aq5P mb', f'scoreboard players operation #azCtxGrp mb = {grp_var} mb',
            'scoreboard players operation #azCtxSide mb = #azSide mb', f'scoreboard players set #azCtxT mb {d["E"]}'])
        sub.at(d['call'], f'execute facing entity {PL} feet rotated ~ 0 run {fn}')
    sub.write()
    for t in sub.ticks():
        tl.at(t, at_paw + sub.fn(t))
    tl.at(60, g.release())
    tl.at(c['end'], 'kill @e[tag=rlk_mb_az_p5m]', g.end())
    tl.write(start, head(p, 'tick') + [g.set_len(c['end'])])
    g.pw(key, 'cancel', cancel_lines(pid))


P5_SLAM = HB.P5['ev']['slam']
LIFT_LEAD = 2          # FIX FAIR-7: the P5 lift sound this many ticks before the clip's lift (t3: 14 t before w1)


# ========================================================================================= P5b triple stomp (id 10)
def emit_stomp3(g):
    p, c = P(10), HB.P5B
    key, pid = p.key, p.id
    tl = A.TL(g, key)
    start = head(p, 'start (#azPT 0; stomp3_<paw A> by #azPaw: 1 fl, 2 fr)') + [
        'scoreboard players operation #aq10P mb = #azPaw mb',
        'execute unless score #aq10P mb matches 1..2 run scoreboard players set #aq10P mb 1',
        'kill @e[tag=rlk_mb_az_p10m]']
    for n, clip in ((1, 'stomp3_fl'), (2, 'stomp3_fr')):
        for i, (s, f) in enumerate(HB.STOMP3_PAW[clip]):
            start.append(f'execute if score #aq10P mb matches {n} positioned {loc(s, f)} run {marker(pid, f"s{i + 1}", "~ 201 ~")}')
    gvars = ('#aq10G1', '#aq10G2', '#aq10G3')
    for i, strike in enumerate(c['strikes']):
        sub = HB.Sub(g, key, f's{i + 1}')
        made = strike - c['tell']
        g.wave(sub, strike, HB.P5['r0'], HB.P5['r1'], None, HB.P5['band'], c['tell'], DMG[c['dmg']], el='ground', grp='new',
               low=HB.P5['low'], ease=HB.P5['ease'], wid=c['wid'][i], tag=f'rlk_mb_az_p10w{i + 1}')
        sub.at(made, g.tag_last_hz('rlk_mb_az_p10'), g.tag_last_hz('rlk_mb_az_p10h'), keep_grp(gvars[i]),
               *hz(g, pid, L.hz_disc(c['slam_r'], c['tell'], DMG[c['dmg']]), grp='cur'))
        sub.at(strike, g.snd('stomp_slam'))            # (FIX FID-1) on the paw's contact, with the impact
        sub.at(strike, g.fxe('impact', 'ground'), g.snd('stomp_wave'))
        # the leg-element splash wall at the ring edge (+5; Hydro: splash_wall, else the element dust ring)
        sub.at(strike + c['splash'], f'execute if score #azE mb matches 2 run {g.fx("splash_wall", r=6.5)}',
               *[f'execute unless score #azE mb matches 2 run {ln}' for ln in A._flat([g.fxe('dust_ring', 'ground', r=6.5)])])
        # the paw's lift (the readable tell: s1 the clip `lift`, s2 / s3 the next paw rising >= 12 t before its slam)
        sub.at(c['ev']['lift'] if i == 0 else c['lifts'][i], g.sound('block.deepslate.step', 1.0, 0.6))
        point = {0: 'stomp3/s1', 2: 'stomp3/s3'}.get(i)
        if point:
            d = A.ADDON_POINTS[point]
            fn = addon_fn(g, key, 'ax_' + d['event'], point, [
                'scoreboard players operation #azCtxPaw mb = #aq10P mb', f'scoreboard players operation #azCtxGrp mb = {gvars[i]} mb',
                'scoreboard players operation #azCtxSide mb = #azSide mb', f'scoreboard players set #azCtxT mb {d["E"]}'])
            sub.at(d['call'], f'execute facing entity {PL} feet rotated ~ 0 run {fn}')
        sub.write()
        for t in sub.ticks():
            tl.at(t, f'execute at @e[type={MK},tag=rlk_mb_az_p10s{i + 1},limit=1] run {sub.fn(t)}')
    tl.at(76, g.release())
    tl.at(c['end'], 'kill @e[tag=rlk_mb_az_p10m]', g.end())
    tl.write(start, head(p, 'tick') + [g.set_len(c['end'])])
    g.pw(key, 'cancel', cancel_lines(pid))


# ================================================================================================= P6 feint (id 6)
def emit_feint(g):
    p, c = P(6), HB.P6
    key, pid, st = p.key, p.id, c['strip']
    tl = A.TL(g, key)
    tell = c['burst'] - c['made']
    start = head(p, 'start (#azPT 0; feint: sways 0 / 12, burst 22). No decal (Change note 1): the sways are the tell') + [
        g.GRP_NEW, keep_grp('#aq6G')]
    # the flank strips, nododge, KB outward (each strip aimed outward: #hzKBDir 1 = along the aim)
    for side, yaw in ((1, -90), (-1, 90)):
        start += hz(g, pid, L.hz_line(st['len'], st['w'], tell, DMG[c['dmg_strip']]), nd=1, kb=KB[c['kb']], kbdir=1,
                    pos=f'execute positioned {loc(side * st["s0"], st["fc"])} rotated ~{yaw} 0')
    # the front (nose) and back (tail root) discs, dodgeable, same group
    for f in (c['nose_f'], c['back_f']):
        start += hz(g, pid, L.hz_disc(c['end_r'], tell, DMG[c['dmg_end']]), pos=f'execute positioned {loc(0, f)}')
    # (FIX FAIR-11) dust shaken off both flanks with each sway (t0 and the swayback t12): a body cue readable from the
    # first tick (the plates' roll reaches 0.5 b only at t7; the strips are #hzNoDodge, 20 t floor)
    sway_dust = [f'execute positioned {loc(sd * 3.4, 0.0)} positioned ~ ~1.6 ~ run {g.fx("dust")}' for sd in (1, -1)] + [
        f'execute positioned {loc(sd * 3.0, f)} positioned ~ ~2.2 ~ run '
        + g.particle('falling_dust{block_state:"minecraft:tuff"}', delta=(0.5, 0.8, 1.2), speed=0.0, n=8)
        for sd in (1, -1) for f in (-1.5, 1.5)]
    start += [g.snd('feint_sway')] + sway_dust
    tl.at(c['ev']['swayback'], g.snd('feint_sway'), *sway_dust)
    tl.at(c['ev']['drop'], g.sound('block.deepslate.break', 1.0, 0.5))
    b = c['burst']
    burst = [g.snd('feint_burst')]
    for side in (1, -1):
        # blades lean to the executor's left: the left strip runs forward from its back end, the right one backward
        yaw, f0 = (0, st['f0']) if side == 1 else (180, st['f1'])
        mid = side * (st['s0'] + st['s1']) / 2
        burst += [f'execute positioned {loc(mid, f0)} rotated ~{yaw} 0 run {ln}'
                  for ln in A._flat([g.fxe('flank_blades', 'ground', len=st['w']), g.fx('dust_wall', len=st['w'])])]
    for f, yaw in ((c['nose_f'], 0), (c['back_f'], 180)):
        burst += [f'execute positioned {loc(0, f)} rotated ~{yaw} 0 run {ln}' for ln in A._flat([g.fxe('slab_throw', 'ground')])]
    # (FIX STATE-2) the dust walls 1 t after the blades and slabs (the burst tick went over 3000 commands)
    walls = [ln for ln in burst if 'dust_wall' in ln]
    tl.at(b, *[ln for ln in burst if 'dust_wall' not in ln])
    tl.at(b + 1, *walls)
    for side in (1, -1):
        yaw, f0 = (0, st['f0']) if side == 1 else (180, st['f1'])
        tl.at(b + 9, f'execute positioned {loc(side * 6.5, f0)} rotated ~{yaw} 0 run {g.fx("dust_wall", len=st["w"])}')
    tl.at(b + 1, g.release())
    tl.at(c['end'], g.end())
    tl.write(start, head(p, 'tick') + [g.set_len(c['end'])])
    g.pw(key, 'cancel', cancel_lines(pid))


# ================================================================================================ P7 tail whip (id 7)
def emit_whip(g):
    p, c = P(7), HB.P7
    key, pid = p.key, p.id
    tl = A.TL(g, key)
    frame = f'@e[type={MK},tag=rlk_mb_az_p7f,limit=1]'
    start = head(p, 'start (#azPT 0; tail_whip_<side> by #azSide; the core drives the yaw schedule). No decal') + [
        'scoreboard players operation #aq7S mb = #azSide mb',
        'execute unless score #aq7S mb matches -1 run scoreboard players set #aq7S mb 1',
        'kill @e[tag=rlk_mb_az_p7m]', marker(pid, 'f'), f'execute as {frame} run tp @s ~ ~ ~ ~ 0',
        'execute store result score #aq7Y mb run data get entity @s Rotation[0]',
        g.snd('whip_raise')]
    for side, sname in ((1, 'l'), (-1, 'r')):
        geo = HB.whip_geom(side)
        sub = HB.Sub(g, key, sname)
        sub.at(c['made'], g.GRP_NEW, keep_grp('#aq7G'))
        for w in geo['wedges']:            # per-tick swept wedge: sector r 12 about the tail root of tick t, one group
            sub.at(w['t'] - c['tell'], *hz(g, pid, L.hz_sector(c['reach'], w['half'], c['tell'], DMG[c['dmg_sweep']]), el=5, nd=1,
                                           kb=KB[c['kb']], kbdir=0, grp='#aq7G',
                                           pos=f'execute positioned {loc(w["s"], w["f"])} rotated ~{w["mid"]} 0'))
            if w['rr'] >= 1.0:             # + the tail base passing the root of tick t (h_pb.whip_geom)
                sub.at(w['t'] - c['tell'], *hz(g, pid, L.hz_disc(w['rr'], c['tell'], DMG[c['dmg_sweep']]), el=5, nd=1,
                                               kb=KB[c['kb']], grp='#aq7G', pos=f'execute positioned {loc(w["s"], w["f"])}'))
        lines = []
        for s, f in geo['erupt']:            # the end-line eruption discs (dodgeable, same group: one hit at most)
            lines += hz(g, pid, L.hz_disc(c['erupt_r'], c['erupt_tell'], DMG[c['dmg_erupt']]), grp='#aq7G',
                        pos=f'execute positioned {loc(s, f)}')
        sub.at(c['erupt'] - c['erupt_tell'], *lines)
        # addon whip/sweep (E 23, call 11): the tail root at E, the start facing, the swept range A0 -> A1
        cs, ce = geo['ctx_sweep'], geo['ctx_end']
        a0, a1, ye = int(round(cs['a0'])), int(round(cs['a1'])), int(round(ce['yaw']))

        def yaw_sc(name, v):
            return ['scoreboard players operation %s mb = #aq7Y mb' % name,
                    f'scoreboard players {"add" if v >= 0 else "remove"} {name} mb {abs(v)}']
        d = A.ADDON_POINTS['whip/sweep']
        fn = addon_fn(g, key, f'ax_sweep_{sname}', 'whip/sweep', [
            'scoreboard players operation #azCtxSide mb = #aq7S mb', 'scoreboard players operation #azCtxGrp mb = #aq7G mb',
            f'scoreboard players set #azCtxT mb {d["E"]}', 'scoreboard players operation #azCtxYaw mb = #aq7Y mb']
            + yaw_sc('#azCtxA0', a0) + yaw_sc('#azCtxA1', a1), yaw_from_ctx=False)
        sub.at(d['call'], f'execute positioned {loc(*cs["pos"])} run {fn}')
        d = A.ADDON_POINTS['whip/end']
        fn = addon_fn(g, key, f'ax_end_{sname}', 'whip/end', [
            'scoreboard players operation #azCtxSide mb = #aq7S mb', 'scoreboard players operation #azCtxGrp mb = #aq7G mb',
            f'scoreboard players set #azCtxT mb {d["E"]}'] + yaw_sc('#azCtxA0', a0) + yaw_sc('#azCtxA1', a1)
            + yaw_sc('#azCtxYaw', ye), yaw_from_ctx=False)
        sub.at(d['call'], f'execute positioned {loc(*ce["pos"])} rotated ~{ce["yaw"]} 0 run {fn}')
        # the sweep's own visual: boulders thrown at the tail tip, grit along the tail line
        for w in geo['wedges']:
            ts, tf = geo['tips'][w['t']]
            if (w['t'] - c['sweep']) % 2 == 0:
                sub.at(w['t'], f'execute positioned {loc(ts, tf)} run {g.fx("boulders")}',
                       f'execute positioned {loc(w["s"], w["f"])} rotated ~{w["mid"]} 0 run {g.fx("tail_lane")}')
        # (FIX STATE-14 / STATE-2) the impact burst at the nearest point, slab throws at the other three: the eruption tick
        # stays inside the 64-card fx cap and the 3000-command tick budget with the sweep's trail cards still alive
        er = [f'execute positioned {loc(s, f)} run {ln}' for i, (s, f) in enumerate(geo['erupt'])
              for ln in A._flat([g.fxe('impact', 'ground') if i == 0 else g.fxe('slab_throw', 'ground')])]
        s1, f1 = geo['erupt'][1]
        sub.at(c['erupt'], *er, f'execute positioned {loc(s1, f1)} run {g.snd("whip_erupt")}')
        sub.write()
        cond = 'if' if side == -1 else 'unless'
        for t in sub.ticks():
            tl.at(t, f'execute {cond} score #aq7S mb matches -1 at {frame} rotated as {frame} run {sub.fn(t)}')
    # (FIX FID-8) a cue a first-person player at the swept flank sees during the raise (t0-20): grit raining off the tail
    # root and dust kicked up along the flank on the side the tail will sweep (the raised tail is above the view)
    for t in (2, 8, 14, 20):
        for side in (1, -1):
            cond = 'if' if side == -1 else 'unless'
            tl.at(t, f'execute {cond} score #aq7S mb matches -1 positioned {loc(side * 3.6, -3.0)} positioned ~ ~0.6 ~ run {g.fx("dust")}',
                  f'execute {cond} score #aq7S mb matches -1 positioned {loc(side * 1.2, -4.6)} positioned ~ ~3.0 ~ run '
                  + g.particle('falling_dust{block_state:"minecraft:tuff"}', delta=(0.6, 0.4, 0.6), speed=0.0, n=10))
    tl.at(c['sweep'], g.snd('whip_sweep'))
    tl.span(c['nopush'][0], c['nopush'][1], 'scoreboard players set #azNoPush mb 1')
    tl.at(c['erupt'] + 1, g.release())
    tl.at(c['end'], 'kill @e[tag=rlk_mb_az_p7m]', g.end())
    tl.write(start, head(p, 'tick') + [g.set_len(c['end'])])
    g.pw(key, 'cancel', cancel_lines(pid))


# ================================================================================================ P8 tail slam (id 8)
def emit_tailslam(g):
    p, c = P(8), HB.P8
    key, pid, hf = p.key, p.id, HB.P8['half']
    tl = A.TL(g, key)
    yh = f'@e[type={MK},tag=rlk_mb_az_p8y,limit=1]'
    t0, t1 = c['turn_ticks'][0], 10
    start = head(p, 'start (#azPT 0; tail_slam). Pre-turn <= 15 deg (t1-10) so the rear axis points at the player') + [
        'kill @e[tag=rlk_mb_az_p8m]',
        'execute store result score #aq8A mb run data get entity @s Rotation[0] 100',
        marker(pid, 'y'), f'execute as {yh} at @s facing entity {PL} feet rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
        f'execute store result score #aq8D mb run data get entity {yh} Rotation[0] 100', 'kill @e[tag=rlk_mb_az_p8y]',
        'scoreboard players operation #aq8D mb -= #aq8A mb',
        'execute if score #aq8D mb matches 18001.. run scoreboard players remove #aq8D mb 36000',
        'execute if score #aq8D mb matches ..-18001 run scoreboard players add #aq8D mb 36000',
        'execute if score #aq8D mb matches 18001.. run scoreboard players remove #aq8D mb 36000',
        'execute if score #aq8D mb matches ..-18001 run scoreboard players add #aq8D mb 36000',
        f'execute if score #aq8D mb matches {int(c["turn_max"] * 100) + 1}.. run scoreboard players set #aq8D mb {int(c["turn_max"] * 100)}',
        f'execute if score #aq8D mb matches ..-{int(c["turn_max"] * 100) + 1} run scoreboard players set #aq8D mb -{int(c["turn_max"] * 100)}',
        'scoreboard players operation #aq8D mb /= #azK10 mb',
        g.snd('tslam_raise')]
    g.pw(key, 'turn', ['# @s = body: one pre-turn step (#aq8D centi-degrees)',
                       'execute store result score #t mb run data get entity @s Rotation[0] 100',
                       'scoreboard players operation #t mb += #aq8D mb',
                       'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #t mb'])
    tl.span(t0, t1, g.fn(f'p/{key}/turn'))
    made = t1
    tell = c['impact'] - made
    # the line from the tail root straight back (len 13, w 3.5) as two outward half-lines: KB sideways (#hzKBDir 1)
    lines = [g.GRP_NEW, keep_grp('#aq8G')]
    for side, yaw in ((1, -90), (-1, 90)):
        lines += hz(g, pid, L.hz_line(hf['len'], hf['w'], tell, DMG[c['dmg']]), kb=KB[c['kb']], kbdir=1,
                    pos=f'execute positioned {loc(side * hf["s0"], hf["fc"])} rotated ~{yaw} 0')
    g.pw(key, 'line', ['# @s = body, rotated as it after the last pre-turn step: the line hazards (one group)'] + lines)
    tl.at(made, f'execute rotated as @s run {g.fn(f"p/{key}/line")}')
    tl.at(c['ev']['hold'], g.snd('tslam_raise'))
    d = A.ADDON_POINTS['tailslam/impact']
    fn = addon_fn(g, key, 'ax_impact', 'tailslam/impact', [
        'scoreboard players operation #azCtxGrp mb = #aq8G mb', f'scoreboard players set #azCtxT mb {d["E"]}',
        'scoreboard players operation #azCtxSide mb = #azSide mb'])
    root = f'execute positioned {loc(0, c["root_f"])} rotated ~180 0'
    tl.at(d['call'], f'{root} run {fn}')
    # (FIX STATE-2) the impact visuals over two ticks: the hit tick keeps the impact and the lane grit; the dust ring and
    # the leaf burst follow 1 t later (one tick of ~32 new cards went over 3000 commands)
    tl.at(c['impact'], g.snd('tslam_impact'),
          *[f'{root} run {ln}' for ln in A._flat([g.fx('tail_lane')])],
          *[f'execute positioned {loc(0, c["root_f"] - 6.5)} run {ln}' for ln in A._flat([g.fxe('impact', 'ground')])])
    tl.at(c['impact'] + 1, *[f'{root} run {ln}' for ln in A._flat([g.fxe('dust_ring', 'ground', r=2.5)])],
          f'execute positioned {loc(0, c["root_f"] - 12.0)} run {g.fx("leaf_burst")}')
    tl.at(c['spikes'], *[f'{root} run {ln}' for ln in A._flat([g.fxe('spike_line', 'ground', len=c['len']), g.fx('cones')])])
    tl.at(c['impact'] + 1, g.release())
    tl.at(c['end'], 'kill @e[tag=rlk_mb_az_p8m]', g.end())
    tl.write(start, head(p, 'tick') + [g.set_len(c['end'])])
    g.pw(key, 'cancel', cancel_lines(pid))


# ============================================================================================ P9 burrow charge (id 9)
def emit_burrow(g):
    p, c = P(9), HB.P9
    key, pid, D = p.key, p.id, {k: DMG[v] for k, v in HB.P9['dmg'].items()}
    tl = A.TL(g, key)
    F = lambda rel: g.fn(f'p/{key}/{rel}')   # noqa: E731
    sel = lambda kind: f'@e[type={MK},tag=rlk_mb_az_p9{kind},limit=1]'   # noqa: E731
    u0, cr = c['u0'], f'{c["ring_r"]}'
    start = head(p, 'start (#azPT 0; burrow_dive -> burrow_travel; ~273 t, plan 5 P9)') + [
        'kill @e[tag=rlk_mb_az_p9m]', 'scoreboard players set #aq9E mb 0', 'scoreboard players set #aq9X mb 0',
        'scoreboard players set #aq9R mb 0', 'scoreboard players set #aq9N mb 0']
    # --- the dive: snarl, dig in, a 3-b glide forward (14 -> 36), proxies inv from 30, hidden from 40
    g0, g1, gd = c['glide']
    tl.at(c['dive']['snarl'], g.sound('entity.ravager.ambient', 1.0, 0.5))
    tl.at(g0, g.snd('burrow_dive'), *g.fxe('dig', 'ground'), f'execute positioned ^ ^ ^{gd} run {marker(pid, "g", "~ 201 ~")}',
          f'execute as {sel("g")} run {g.clamp_body(c["travel_r"])}',
          f'execute at {sel("g")} run function rlk:mboss/mv/glide {{t:{g1 - g0}}}', 'kill @e[tag=rlk_mb_az_p9g]')
    tl.at(24, *g.fxe('dig', 'ground'))
    tl.at(c['inv'], g.px('inv'))
    tl.at(c['dive']['under'], g.fx('mound'), *g.fxe('dust_ring', 'ground', r=3.0),
          # the edge flag: the target farther than 20 b from the centre at the dive
          f'execute at {A.ARENA_M} unless entity {PL.replace("limit=1", "distance=..%s,limit=1" % int(c["edge_r"]))} '
          'run scoreboard players set #aq9E mb 1')
    # --- underground: the anchor glides hidden toward the player (0.3 b/t, clamp r 12), the dig loop every 30 t
    g.pw(key, 'under', ['# @s = body (hidden): 0.3 b/t toward the player, kept within r 12 of the centre',
                        f'execute facing entity {PL} feet rotated ~ 0 positioned ^ ^ ^{c["travel"]} run tp @s ~ ~ ~',
                        g.clamp_body(c['travel_r'])])
    busy = set()
    for a, b in zip(c['rush_clip'], c['rush_end']):
        busy |= set(range(a, b + 1))
    free, run = [], None
    for t in range(u0 + 1, c['emerge_t']):
        if t in busy:
            run = None
        elif run is None:
            run = [t, t]
            free.append(run)
        else:
            run[1] = t
    under = [f'execute if score #azPT mb matches {a}..{b} run {F("under")}' for a, b in free]
    for t in range(u0, c['emerge_t'], 30):
        tl.at(t, g.snd('burrow_loop'))
    # --- rock rings (keep: the chevron ring outline from the decision, tell 19) under lockv lead 6, own groups
    g.pw(key, 'ring_at', ['# At a ring point: the hazard r 3.4 (own group) + its kit ring outline (keep), the ring sound, the shaft']
         + hz(g, pid, L.hz_disc(c['ring_r'], c['ring_tell'], D['ring']), el=5, grp='new', extra=('rlk_mb_az_p9ring',))
         + [K.tele_disc(c['ring_r'], c['ring_tell'], el=5, fill=0, style='chev'), g.snd('burrow_ring'), g.fx('light_shaft')])
    g.pw(key, 'ring_hit', ['# At a ring point at its hit: the rock lands', g.snd('burrow_rock')] + A._flat([g.fxe('impact', 5)])
         + [g.fx('dust')])
    for i, t in enumerate(c['ring_t']):
        tag = f'r{i + 1}'
        tl.at(t, *g.lockv(c['ring_lead']), *g.keep(f'rlk_mb_az_p9{tag}'), f'execute at {sel(tag)} run {F("ring_at")}')
        tl.at(t + c['ring_tell'] - 6, f'execute at {sel(tag)} run {g.fx("rock_rain", r=c["ring_r"])}')
        tl.at(t + c['ring_tell'], f'execute at {sel(tag)} run {F("ring_hit")}', f'kill @e[tag=rlk_mb_az_p9{tag}]')
    # --- small rocks with ring A1: r 1.4 at +3 / +6 / +9 b along the player's velocity (else anchor -> lock), one
    #     group, tell 14; falling-rock props over each point for the whole 14 t (the readable tell, Change note 1)
    t_r = c['rock_t']
    g.pw(key, 'rocks_at', ['# At the ring-A1 point, rotated along the velocity line: three rock points (+3 / +6 / +9 b)', g.GRP_NEW,
                           keep_grp('#aq9GR')]
         + [f'execute positioned ^ ^ ^{d} run {F("rock_one")}' for d in c['rock_d']])
    g.pw(key, 'rock_one', ['# One rock point (clamped into the walk disc): its hazard and its falling prop.',
                           marker(pid, 'rn', '~ 201 ~'), f'execute as {sel("rn")} run {g.clamp_walk()}',
                           f'execute at {sel("rn")} run {F("rock_mk")}', 'tag @e[tag=rlk_mb_az_p9rn] add rlk_mb_az_p9rk',
                           'tag @e[tag=rlk_mb_az_p9rn] remove rlk_mb_az_p9rn'])
    g.pw(key, 'rock_mk', ['# The rock hazard (the current group) and the rock prop 14 b up (falls 1 b/t)']
         + hz(g, pid, L.hz_disc(c['rock_r'], c['rock_tell'], D['rock']), el=5, grp='cur')
         + [f'summon minecraft:item_display ~ ~{c["rock_tell"]} ~ {{{tags(pid, "rp").replace("]", ",\"rlk_mb_az_p9rpn\"]")},'
            'billboard:"center",teleport_duration:1,view_range:3f,'
            'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.8f,1.8f,1.8f]}}',
            f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p9rpn] run {K.look("boulder")}',
            'tag @e[type=minecraft:item_display,tag=rlk_mb_az_p9rpn] remove rlk_mb_az_p9rpn'])
    tl.at(t_r, f'execute if score #mbV mb matches 81.. at {sel("r1")} facing entity {PL} feet rotated ~180 0 run {F("rocks_at")}',
          f'execute unless score #mbV mb matches 81.. at {sel("r1")} facing entity @s feet rotated ~180 0 run {F("rocks_at")}')
    tl.span(t_r + 1, t_r + c['rock_tell'] - 1,
            'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p9rp] at @s run tp @s ~ ~-1 ~')
    tl.at(t_r + c['rock_tell'], f'execute at @e[type={MK},tag=rlk_mb_az_p9rk] run {g.fx("dust")}',
          f'execute at @e[type={MK},tag=rlk_mb_az_p9rk] run {g.snd("burrow_rock")}',
          'kill @e[tag=rlk_mb_az_p9rp]', 'kill @e[tag=rlk_mb_az_p9rk]')
    # --- surfacing rushes: the breach point 6 b from the player toward the anchor (rush 2 with the edge flag: the
    #     centre), the lane toward the player; the mound / bulge / rumble there for 20 t (the readable tell), then
    #     burrow_breach so its `hit` is the first hit; the disc r 3.0 rides the body 20 t at 0.6 b/t
    g.pw(key, 'rush_pick', [
        '# @s = body: the breach point (rush #aq9N) and the rush hazard there (own group, tell 20, 21 t of hits)',
        'kill @e[tag=rlk_mb_az_p9b]',
        f'execute unless score #aq9N mb matches 2 at {PL} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{c["rush_off"]} '
        f'run {marker(pid, "b", "~ 201 ~")}',
        f'execute if score #aq9N mb matches 2 unless score #aq9E mb matches 1 at {PL} facing entity @s feet rotated ~ 0 '
        f'positioned ^ ^ ^{c["rush_off"]} run {marker(pid, "b", "~ 201 ~")}',
        f'execute if score #aq9N mb matches 2 if score #aq9E mb matches 1 at {A.ARENA_M} run {marker(pid, "b", "~ 201 ~")}',
        f'execute as {sel("b")} run {g.clamp_body(c["safe_r"])}',
        f'execute as {sel("b")} at @s facing entity {PL} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
        f'execute at {sel("b")} run {F("rush_hz")}'])
    g.pw(key, 'rush_hz', ['# At the breach point: the rush hazard (moved onto the body from its hit on)']
         + hz(g, pid, L.hz_disc(c['rush_r'], c['rush_tell'], D['rush']), el=5, grp='new', act=c['rush_act'],
              extra=('rlk_mb_az_p9rush',)) + [g.fx('mound'), g.snd('burrow_loop')])
    g.pw(key, 'rush_tell', ['# At the breach point during the 20-t tell: the bulge / dust plume and the rumble',
                            g.fx('mound'), g.fx('dust'), g.sound('block.rooted_dirt.break', 1.0, 0.5),
                            g.sound('entity.warden.dig', 0.8, 0.5)])
    g.pw(key, 'rush_go', ['# @s = body: to the breach point, facing the lane; burrow_breach (hidden until its burst)',
                          f'execute at {sel("b")} rotated as {sel("b")} run tp @s ~ ~ ~ ~ 0', g.play('burrow_breach')])
    g.pw(key, 'rush_step', ['# @s = body: 0.6 b/t along the lane (inside the arena), the rush disc rides the body',
                            f'execute at @s positioned ^ ^ ^{c["rush_spd"]} if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
                            f'execute at @s as @e[type={MK},tag=rlk_mb_az_p9rush] run tp @s ~ ~ ~',
                            '# (FIX STATE-2 / STATE-14) the dust trail every other tick (3 cards each, life 14)',
                            'scoreboard players operation #aq9Q mb = #azPT mb', 'scoreboard players operation #aq9Q mb %= #c2 mb',
                            f'execute if score #aq9Q mb matches 0 at @s run {g.fx("dust")}'])
    for n, (t, tc, th, te) in enumerate(zip(c['rush_t'], c['rush_clip'], c['rush_hit'], c['rush_end']), 1):
        tl.at(t, f'scoreboard players set #aq9N mb {n}', F('rush_pick'))
        for k in range(t, tc + 8, 5):
            tl.at(k, f'execute at {sel("b")} run {F("rush_tell")}')
        tl.at(tc, F('rush_go'))
        tl.at(tc + c['breach']['burst'], g.snd('burrow_rush'), g.fxe('impact', 5), g.fx('mound'))
        tl.span(th + 1, te, F('rush_step'))
        tl.at(te, g.fx('mound'), 'kill @e[tag=rlk_mb_az_p9b]')
    # --- the final emergence: the spot at u160 (lockv lead 8; edge flag: the centre); the mound / spires / rumble and
    #     the burst hazard from 19 t before the burst; burrow_emerge at u180 (burst 8, proxies normal at out 38)
    tf, tm, te, tb, to = c['final_t'], c['mound_t'], c['emerge_t'], c['burst_t'], c['out_t']
    tl.at(tf, f'execute unless score #aq9E mb matches 1 run {F("final_lock")}',
          f'execute if score #aq9E mb matches 1 at {A.ARENA_M} run {marker(pid, "e", "~ 201 ~")}')
    g.pw(key, 'final_lock', ['# The emergence spot under lockv lead 8 (re-tagged rlk_mb_az_p9e)'] + g.lockv(c['emerge_lead'])
         + g.keep('rlk_mb_az_p9e') + ['tag @e[tag=rlk_mb_az_p9e] add rlk_mb_az_p9m'])
    tl.at(tm, f'execute at {sel("e")} run {F("burst_hz")}')
    g.pw(key, 'burst_hz', ['# At the emergence spot: the burst hazard r 3.7 (own group, tell 19, no decal)']
         + hz(g, pid, L.hz_disc(c['burst_r'], c['burst_tell'], D['burst']), el=5, grp='new'))
    g.pw(key, 'mound', ['# The emergence precursor at the spot: dust mound, spires of grit, rumble',
                        g.fx('mound'), g.fx('dust'), g.sound('entity.warden.dig', 1.0, 0.5), g.sound('block.rooted_dirt.break', 1.0, 0.6)])
    for k in range(tm, tb, 4):
        tl.at(k, f'execute at {sel("e")} run {F("mound")}')
    tl.at(te - 1, f'execute at {sel("e")} facing entity {PL} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0')
    tl.at(te, g.play('burrow_emerge'))
    tl.at(tb, f'execute at {sel("e")} run {F("burst_fx")}')
    g.pw(key, 'burst_fx', ['# The emergence burst at the spot', g.snd('burrow_rush'), g.fx('emerge_spikes', r=c['burst_r']),
                           g.fx('mound')])
    tl.at(to, g.px('normal'))
    tl.at(to + 1, f'execute unless score #aq9E mb matches 1 run {g.release()}')
    tl.at(c['end'], f'execute unless score #aq9E mb matches 1 run {F("fin")}')
    g.pw(key, 'fin', ['# The pattern ends: its markers and props go', 'kill @e[tag=rlk_mb_az_p9m]', g.end()])
    # --- edge flag: the centre run (reads like P3: facing + growl 20 t, then 1.0 b/t toward the target, len dist + 4)
    tr = c['run_face']
    g.pw(key, 'run_pick', [
        '# @s = body (emerged at the centre): face the target, growl; the run length #aq9R = dist + 4 b (<= 24 t); the',
        '# run disc r 4 rides the body from its first hit (tell 20); the pattern end = the run end + charge_stop.',
        'function rlk:mboss/mv/face', g.snd('charge_growl'), 'function rlk:mboss/mv/dist',
        'scoreboard players operation #aq9R mb = #mbDist mb', 'scoreboard players add #aq9R mb 49',
        'scoreboard players operation #aq9R mb /= #azK10 mb',
        f'execute if score #aq9R mb matches {c["run_max"] + 1}.. run scoreboard players set #aq9R mb {c["run_max"]}',
        'scoreboard players operation #aq9X mb = #aq9R mb', f'scoreboard players add #aq9X mb {to + 1 + 21}',
        'scoreboard players operation #azPLen mb = #aq9X mb']
        + hz(g, pid, L.hz_disc(c['run_r'], c['run_tell'], D['run']), el=5, grp='new', act=c['run_max'] + 1,
             extra=('rlk_mb_az_p9run',)))
    g.pw(key, 'run_step', ['# @s = body: one run tick (1.0 b/t while inside the arena), the disc rides the body; at the end',
                           '# the disc ends and charge_stop plays.',
                           'scoreboard players remove #aq9R mb 1',
                           f'execute at @s positioned ^ ^ ^{c["run_spd"]} unless function rlk:mboss/mv/ok run scoreboard players set #aq9R mb 0',
                           f'execute if score #aq9R mb matches 0.. at @s positioned ^ ^ ^{c["run_spd"]} if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
                           f'execute at @s as @e[type={MK},tag=rlk_mb_az_p9run] run tp @s ~ ~ ~',
                           'scoreboard players set #azNoPush mb 1',
                           *g.every(4, g.fx('dust_trail')), f'execute if score #azM mb matches 0 run {g.snd("charge_gallop")}',
                           f'execute if score #aq9R mb matches ..0 run {F("run_stop")}'])
    g.pw(key, 'run_stop', ['# @s = body: the run ends (disc gone, skid, charge_stop); the pattern ends 21 t later',
                           f'execute as @e[type={MK},tag=rlk_mb_az_p9run] at @s rotated as @s run function rlk:mboss/hz/expire',
                           'scoreboard players set #aq9R mb -1', 'scoreboard players operation #aq9X mb = #azPT mb',
                           'scoreboard players add #aq9X mb 21', 'scoreboard players operation #azPLen mb = #aq9X mb',
                           g.play('charge_stop'), g.snd('charge_skid'), g.fx('skid'), g.release()])
    tl.at(tr, f'execute if score #aq9E mb matches 1 run {F("run_pick")}')
    tl.at(to, f'execute if score #aq9E mb matches 1 run {g.play("charge_run")}')
    tick_head = head(p, 'tick') + under + [
        # the edge run (dynamic length): one step per tick while #aq9R >= 1 from `out`; the end when #aq9X is reached
        f'execute if score #aq9E mb matches 1 if score #azPT mb matches {to + 1}.. if score #aq9R mb matches 1.. run {F("run_step")}',
        f'execute if score #aq9E mb matches 1 if score #aq9X mb matches 1.. if score #azPT mb >= #aq9X mb run return run {F("fin")}']
    tl.write(start + [g.set_len(c['end'])], tick_head)
    # resume: the live rock-ring outlines (keep rows) are redrawn with their remaining tell (the kit cleared them)
    g.pw(key, 'resume', ['# @s = body: redraw the live rock-ring outlines (keep) with the remaining tell',
                         f'execute as @e[type={MK},tag=rlk_mb_az_p9ring] at @s run {F("ring_redraw")}'])
    g.pw(key, 'ring_redraw', ['# @s = a live ring hazard: the outline again for its remaining tell',
                              'scoreboard players operation #t mb = @s mbHzW', 'scoreboard players operation #t mb -= @s mbHzT',
                              'execute if score #t mb matches ..0 run return 0',
                              f'data modify storage rlk:mboss az.tl set value {{r:{int(round(c["ring_r"] * 10))},el:5,nd:0,hold:3}}',
                              'execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #t mb',
                              (f'function {K.FN}tele/chev_o with storage rlk:mboss az.tl' if A.KIT else K._c('tele/disc'))])
    g.pw(key, 'cancel', cancel_lines(pid, [
        '# the body comes back up (fight state only: death sets its own proxy state)',
        f'execute if score #mbSt mb matches 1 run {g.px("normal")}',
        f'execute if score #mbSt mb matches 1 as {BODY} run {g.play("idle")}']))


def emit(g):
    emit_stomp(g)
    emit_stomp3(g)
    emit_feint(g)
    emit_whip(g)
    emit_tailslam(g)
    emit_burrow(g)
