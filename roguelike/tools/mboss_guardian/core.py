"""Corrupted Guardian core: hooks, AI, rotation, guard mode, chaos, groggy, entrance, death, HUD,
voice lines, tests and the generated pattern dispatchers. See __init__.py for the package layout
and the scratchpad file mboss/gd_contract.md for the core <-> pattern contract.

Owns F:mboss/guardian/** except F:mboss/guardian/rig/** (tools/build_mboss_guardian_rig.mjs).
Every file it owns is deleted and rewritten on each run.
"""
import importlib
import math

from . import PATTERN_MODULES
from . import api as A
from .api import L, Gen, ev, clip_len, DMG, KB, CX, CY, CZ

NS = A.NS
OWN_TOP = 'mboss/' + A.ID

# ---------------------------------------------------------------------------------------------
# Tunables (plan.md K3-K24; patterns.md §8-§11)
GUARD_ENTRY = clip_len('guard_entry')        # 50 t twirl, discs, ground ring, settle
GUARD_ACTIVE = 100                            # PDF 5 s
GUARD_END = GUARD_ENTRY + GUARD_ACTIVE        # guard clock tick of the timeout
GUARD_GAP = {1: 20, 2: 20}                    # after the sweep clip: guard I -> guard II, guard II -> chaos
REC_NEW, REC_AGAIN, REC_GAP = 3, 9, 8         # hits to record / re-record, one count per element per 8 t
CHAOS_TIMER = 350                             # 17.5 s
CHAOS_NEAR = 6.0                              # nearer than this to the centre: glide instead of the leap
STAR_DIST, STAR_ANGLE = 4.2, 55               # stars 4.2 b from the body, +-55 degrees off her facing
STAR_PM = {'active': 70, 'inert': 17}         # star pools, per mille of the body's max HP (K8)
STAR_RES_INERT = 80                           # inert stars: all RES +80 % (x0.238)
IMMUNE_PCT = 0                                # % of an own-element hit an active star takes (0 = immune)
BREAK_DELAY = 5                               # star break -> boss damage (S+5)
BREAK_PCT = (6, 18)                           # 1st / 2nd star break, % of the boss's max HP
GROGGY = 220                                  # K13
NEXT_AFTER_CHAOS = (4, 5)                     # normal patterns before the next guard pair
OPENING = (3, 4)
VOICE_CD, VOICE_GUARD_CD = 400, 600
INTRO_TELL, INTRO_CLIP = 16, 26               # intro clock: ground telegraph, entrance clip start
INTRO_IMPACT = INTRO_CLIP + ev('entrance', 'impact')
INTRO_DONE = 66
DEATH_LEN = clip_len('death')

ST = {'idle': 0, 'pattern': 1, 'close': 2, 'guard': 3, 'chaos': 4, 'groggy': 5, 'approach': 6, 'dead': 7}


def build():
    out = L.Out()
    g = Gen(out)
    pats = []
    for name in PATTERN_MODULES:
        mod = importlib.import_module(f'{__package__}.{name}')
        for p in mod.PATTERNS:
            p.module = name
        pats.extend(mod.PATTERNS)
        mod.emit(g)
    ids = [p.id for p in pats]
    assert len(set(ids)) == len(ids), ids
    keys = [p.key for p in pats]
    assert len(set(keys)) == len(keys), keys
    for p in pats:
        for f in ('start', 'tick', 'cancel'):
            assert g.has(f'p/{p.key}/{f}'), f'{p.module}: pattern {p.key} has no {f}'
    for need in (1, 2, 3, 4, 5, 11, 12, 13):
        assert need in ids, f'pattern id {need} missing'
    normal = [p for p in pats if p.kind == 'normal']
    Core(g, pats, normal).emit()
    removed = clean(out)
    print(f'mboss guardian: {len(g.files)} functions ({len(normal)} normal + {len(pats) - len(normal)} service patterns '
          f'from {", ".join(PATTERN_MODULES)}), {removed} stale removed.')


def clean(out):
    """Owned: every file under F:mboss/guardian/ except rig/ (another generator)."""
    root = L.FN / OWN_TOP
    removed = 0
    for p in sorted(root.rglob('*.mcfunction')):
        rel = p.relative_to(root).as_posix()
        if rel.startswith('rig/'):
            continue
        if p.resolve() not in out.written:
            p.unlink()
            removed += 1
    for p in sorted(root.rglob('*'), reverse=True):
        if p.is_dir() and not p.relative_to(root).as_posix().startswith('rig') and not any(p.iterdir()):
            p.rmdir()
    return removed


# ---------------------------------------------------------------------------------------------
def sc_set(name, v):
    return f'scoreboard players set {name} mb {int(v)}'


def at_t(clock, t, cmd):
    rng = f'{t[0]}..{t[1]}' if isinstance(t, tuple) else str(t)
    return f'execute if score {clock} mb matches {rng} run {cmd}'


class Core:
    def __init__(self, g, pats, normal):
        self.g, self.pats, self.normal = g, pats, normal
        self.F = g.fn
        self.R = g.rig

    def w(self, rel, lines):
        self.g.w(rel, lines)

    # =========================================================================================
    def emit(self):
        self.consts_vars()
        self.hooks()
        self.intro()
        self.ai()
        self.slot()
        self.guard()
        self.chaos()
        self.stars()
        self.groggy()
        self.voice()
        self.hud()
        self.looks()
        self.tests()

    # -----------------------------------------------------------------------------------------
    def consts_vars(self):
        self.w('ai/consts', ['# Module constants (spawn, reload). #gdK<n> are the moduli of Gen.every.']
               + [sc_set(f'#gdK{n}', n) for n in (2, 3, 4, 5, 6, 8, 20)])
        v = ['# Every fake player of the module back to its fight-start value (spawn, reload, cleanup; no executor).',
             '# AI state: 0 idle 1 pattern 2 close-in 3 guard 4 chaos 5 groggy 6 approach 7 dying']
        v += [sc_set(k, 0) for k in ('#gdSt', '#gdT', '#gdLast', '#gdPick', '#gdReq', '#gdPat', '#gdPNew', '#gdPT',
                                      '#gdPEnd', '#gdPMax', '#gdPDone', '#gdMv', '#gdClk', '#gdVoCd', '#gdVoG',
                                      '#gdFlash', '#gdTst', '#gdDist')]
        v += [sc_set('#gdCool', 30), sc_set('#gdBand', 2),
              f'execute store result score #gdLeft mb run random value {OPENING[0]}..{OPENING[1]}']
        v += [sc_set(f'#gdBag{p.id}', 1) for p in self.normal]
        v += ['# guard mode and the element record']
        v += [sc_set(k, 0) for k in ('#gdGN', '#gdGP', '#gdRecOn', '#gdRecNew', '#gdRecEl', '#gdSlotA', '#gdSlotB',
                                      '#gdSwEl', '#gdGW')]
        for e in range(1, 5):
            v += [sc_set(f'#gdN{e}', 0), sc_set(f'#gdQ{e}', REC_NEW), sc_set(f'#gdRc{e}', 0)]
        v += ['# chaos, stars, fail spears']
        v += [sc_set(k, 0) for k in ('#gdCP', '#gdChV', '#gdCh0', '#gdTim', '#gdTimS', '#gdF', '#gdFailN',
                                      '#gdFailK1', '#gdFailK2', '#gdFailDone', '#gdBrk', '#gdBq1', '#gdBq2',
                                      '#gdBe1', '#gdBe2', '#gdStars', '#gdSk1', '#gdSk2', '#gdSa1', '#gdSa2',
                                      '#gdCsT', '#gdHaze')]
        self.w('ai/vars', v)

    # -----------------------------------------------------------------------------------------
    def hooks(self):
        F, R = self.F, self.R
        self.w('spawn', [
            '# Hook spawn (@s = arena marker at the centre, rotated north). The body stands on the centre star facing',
            '# south (the arriving player); the rig spawns hidden and the entrance clip brings it in (intro_tick).',
            'execute rotated 0 0 run function rlk:mboss/body',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("intro/setup")}'])
        self.w('intro_tick', [
            '# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end).',
            f'# {INTRO_TELL}: ground telegraph (24 t) + glint; {INTRO_CLIP}: entrance clip (impact at clip tick '
            f'{ev("entrance", "impact")} = intro {INTRO_IMPACT}); {INTRO_DONE}: fight.',
            '# The rig is not ticked before the clip starts, so the hidden parts stay hidden.',
            at_t('#mbT', INTRO_TELL, F('intro/tell')),
            at_t('#mbT', INTRO_CLIP, self.g.play('entrance')),
            at_t('#mbT', INTRO_CLIP, F('intro/fall')),
            at_t('#mbT', (INTRO_CLIP, 999), R('tick')),
            at_t('#mbT', (INTRO_CLIP + 1, INTRO_IMPACT - 1), F('intro/trail')),
            at_t('#mbT', INTRO_IMPACT, F('intro/impact')),
            at_t('#mbT', INTRO_CLIP + ev('entrance', 'grab'), A.Gen.sound('item.armor.equip_netherite', 0.6, 1.3)),
            at_t('#mbT', INTRO_CLIP + ev('entrance', 'pull'), F('intro/pullout')),
            at_t('#mbT', (INTRO_DONE, 999), F('intro/done'))])
        self.w('tick', [
            '# Hook tick (@s = body, at @s, fight state). Order: clocks, stars and their queued punishments (true',
            '# damage, can be lethal), AI state, pattern slot, then the rig (a clip played this tick starts this tick).',
            'scoreboard players add #gdClk mb 1',
            'execute if score #gdVoCd mb matches 1.. run scoreboard players remove #gdVoCd mb 1',
            'execute if score #gdVoG mb matches 1.. run scoreboard players remove #gdVoG mb 1',
            f'execute if score #gdFlash mb matches 1 unless score @s gdRigF matches 1.. run {R("flash")}',
            sc_set('#gdFlash', 0),
            f'execute if score #gdStars mb matches 1.. run {F("star/tick")}',
            f'execute if score #gdBq1 mb matches 1.. run {F("star/bq1")}',
            'execute unless score #mbSt mb matches 1 run return 0',
            f'execute if score #gdBq2 mb matches 1.. run {F("star/bq2")}',
            'execute unless score #mbSt mb matches 1 run return 0',
            F('ai/state'),
            f'execute if score #gdPat mb matches 1.. run {F("p/run")}',
            R('tick')])
        on_hit = [
            '# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg known). Flags and scores only.',
            '# Element record (K5): during the guard window, a hit with #elem 1-4 (reaction damage #tfm excluded)',
            f'# counts once per element per {REC_GAP} t; {REC_NEW} hits record a new element, {REC_AGAIN} re-record slot A\'s.',
            sc_set('#gdFlash', 1),
            'execute unless score #gdRecOn mb matches 1 run return 0',
            'execute if score #gdRecNew mb matches 1.. run return 0',
            'execute if score #tfm tmp matches 1 run return 0']
        on_hit += [f'execute if score #elem tmp matches {e} run return run {F(f"rec/e{e}")}' for e in range(1, 5)]
        self.w('on_hit', on_hit)
        for e in range(1, 5):
            self.w(f'rec/e{e}', [
                f'# One counted {A.EL_KEY[e]} hit (at most one per {REC_GAP} t of the fight clock #gdClk).',
                f'execute if score #gdClk mb < #gdRc{e} mb run return 0',
                f'scoreboard players operation #gdRc{e} mb = #gdClk mb',
                f'scoreboard players add #gdRc{e} mb {REC_GAP}',
                f'scoreboard players add #gdN{e} mb 1',
                f'execute if score #gdN{e} mb >= #gdQ{e} mb run scoreboard players set #gdRecNew mb {e}'])
        self.w('aux_hit', [
            '# Hook aux_hit (@s = a star inside combat/apply; #dmg already modified like a body hit, RES included:',
            f'# inert stars carry mres {STAR_RES_INERT}). Outside a running chaos timer the star takes nothing (no number);',
            '# an active star is immune to its own element (framework "면역" popup when #dmg is 0).',
            f'execute unless score #mbSt mb matches 1 run return run {F("star/ignore")}',
            f'execute unless score #gdSt mb matches 4 run return run {F("star/ignore")}',
            f'execute unless score #gdCP mb matches 3 run return run {F("star/ignore")}',
            'execute unless entity @s[tag=rlk_mb_gd_star] run return 0',
            f'execute if score @s mbS matches 1..4 if score #elem tmp = @s mbS run {F("star/immune")}'])
        self.w('incoming', [
            '# Hook incoming (@s = body inside combat/apply_mods, after level and RES): no extra modifiers.',
            '# Groggy has no damage bonus (PDF "추가 내성 감소 없음") and the boss keeps base RES in chaos (K7).'])
        self.w('pause', ['# Hook pause: the framework freezes AI, hazards and props; the rig holds its last key.',
                         '# The running pattern may drop what would hang in the world meanwhile (its optional pause).',
                         sc_set('#gdFlash', 0),
                         F('p/pause_d')])
        self.w('resume', ['# Hook resume: nothing to restore (module timers live in the body tick and simply continue).'])
        self.w('death_start', [
            '# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden).',
            F('p/cancel'),
            F('chaos/reset'),
            sc_set('#gdSt', ST['dead']),
            sc_set('#gdRecOn', 0), sc_set('#gdBq1', 0), sc_set('#gdBq2', 0),
            R('spear/geo'), R('eye/geo'),
            self.g.play('death'),
            F('voice/death'),
            A.Gen.sound('entity.wither.ambient', 0.25, 1.6)])
        trail = ['# Hook death_tick (@s = body, #mbT = 1.. until cur.death): slump, fly-away with a cube trail, fade.',
                 f'# The rig must tick for the clip to run, and must NOT tick after its kill at {DEATH_LEN} (it would respawn).',
                 at_t('#mbT', (1, DEATH_LEN - 1), R('tick')),
                 at_t('#mbT', DEATH_LEN, R('kill')),
                 at_t('#mbT', 4, A.Gen.sound('block.amethyst_block.fall', 0.7, 0.6)),
                 at_t('#mbT', ev('death', 'takeoff'), A.Gen.sound('entity.ender_dragon.flap', 0.8, 1.3)),
                 at_t('#mbT', ev('death', 'takeoff'), A.Gen.sound('item.trident.riptide_3', 0.7, 1.0))]
        # rise of the clip (pos y keys 22: 0.22, 30: 1.6, 56: 9.0, 76: 15.0)
        keys = [(22, 0.22), (30, 1.6), (56, 9.0), (76, 15.0)]
        for t in range(22, 77, 2):
            for (t0, y0), (t1, y1) in zip(keys, keys[1:]):
                if t0 <= t <= t1:
                    y = y0 + (y1 - y0) * (t - t0) / (t1 - t0)
            pos = f'~ ~{L.num(y + 1.2, 2)} ~'
            trail.append(at_t('#mbT', t, self.g.dust_fade(A.RED_EDGE, A.CRIMSON_DARK, 1.4, pos, (0.35, 0.5, 0.35), 6)))
            if t % 4 == 0:
                trail.append(at_t('#mbT', t, self.g.particle('block{block_state:"minecraft:gold_block"}', pos, (0.3, 0.4, 0.3), 0, 3)))
        trail.append(at_t('#mbT', 60, self.g.particle('end_rod', '~ ~14 ~', (0.6, 1.0, 0.6), 0.02, 12)))
        self.w('death_tick', trail)
        self.w('cleanup', [
            '# Hook cleanup (no executor; idempotent): module fake players back to their defaults.',
            '# Module entities carry rlk_mb_aux (rig parts, props, stars, fx) and die with the framework sweep.',
            F('ai/vars')])
        self.w('uninstall', [
            '# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props and',
            '# its gdRig* objectives (the framework removes mb and the rlk_mb_aux entities).',
            R('uninstall')])
        self.w('reload', [
            '# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, stars, fx, props).',
            '# AI back to idle with HP kept; a guard pair restarts soon, an interrupted chaos is abandoned.',
            F('ai/consts'),
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            F('p/cancel'),
            'execute if score #gdSt mb matches 3 run scoreboard players set #gdLeft mb 0',
            f'execute if score #gdSt mb matches 4..6 run {F("chaos/reset")}',
            'execute if score #gdSt mb matches 4..6 run scoreboard players set #gdLeft mb 4',
            sc_set('#gdRecOn', 0), sc_set('#gdRecNew', 0), sc_set('#gdBq1', 0), sc_set('#gdBq2', 0),
            sc_set('#gdStars', 0), sc_set('#gdHaze', 0), sc_set('#gdTim', 0),
            sc_set('#mbNoLeash', 0),
            'tag @s remove rlk_mb_inv',
            R('spawn'),
            R('spear/geo'),
            F('look/eye_rest'),
            sc_set('#gdCool', 20),
            F('ai/enter')])
        self.w('bars', [
            '# Hook bars (@s = body, every tick in intro/fight). Under-bar: guard = leading element\'s record progress',
            '# (its colour; gold = guard time left before the first counted hit), chaos = timer (Pyro code 2, D22),',
            '# groggy = time left (green), pattern = progress (gold). Sub-line and name-line glyphs: hud/*.',
            f'execute if score #gdSt mb matches 3 if score #gdGP mb matches 2 run return run {F("hud/bar_guard")}',
            f'execute if score #gdSt mb matches 4 if score #gdCP mb matches 3 run return run {F("hud/bar_chaos")}',
            f'execute if score #gdSt mb matches 5 run return run {F("hud/bar_groggy")}',
            f'execute if score #gdPat mb matches 1.. unless score #gdPNew mb matches 1 run {F("hud/bar_pattern")}'])
        self.w('hz_vis', ['# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end). Visual ids are pattern id x 10 + k.',
                          F('p/vis')])
        self.w('pj_end', ['# Hook pj_end (@s = prop, #pjEv, #pjKeep preset). Routed by the prop\'s mbId (= pattern id).',
                          F('p/pj_end')])
        self.w('test', [
            '# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.',
            '$scoreboard players set #gdTst mb $(id)',
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("test/run")}'])

    # -----------------------------------------------------------------------------------------
    def intro(self):
        F, g = self.F, self.g
        plant = 'rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7'
        self.w('intro/setup', [
            '# @s = the new body (from the spawn hook): module state, hidden rig, HUD.',
            F('ai/consts'), F('ai/vars'),
            self.R('spawn_hidden'),
            F('hud/sub_intro')])
        self.w('intro/tell', [
            '# Entrance telegraph (K19, >= 12 t, a deliberate deviation from the PDF\'s "no sign"): a ground disc where the',
            '# spear will plant (right-front of her, clip grip ^-0.62 ^ ^0.7) and a glint high above it.',
            sc_set('#hzSfx', 1), sc_set('#hzKB', KB['default']),
            f'execute {plant} positioned ~ {CY} ~ run {g.hz_disc(3.0, INTRO_IMPACT - INTRO_TELL, DMG["entrance"])}',
            f'execute {plant} run ' + g.card('star', '^ ^7.4 ^', bb='center', spin=90, s0=0.2, s1=1.4, life=14, fade=6),
            f'execute {plant} run ' + g.sound('block.amethyst_block.chime', 1.0, 1.8),
            f'execute {plant} run ' + g.sound('block.beacon.power_select', 0.4, 1.9)])
        self.w('intro/fall', [f'execute {plant} run ' + g.sound('block.beacon.deactivate', 0.6, 1.8)])
        self.w('intro/trail', [f'execute {plant} run ' + g.dust(A.GOLD, 1.2, '^ ^4 ^', (0.1, 2.5, 0.1), 4)])
        self.w('intro/impact', [
            '# The plant (clip tick 14): gold pillar, ground ring, radial crystal blades, the start line.',
            f'execute {plant} positioned ~ {CY} ~ run ' + g.card('burst', '^ ^1.2 ^', bb='center', spin=20, s0=0.8, s1=3.2, life=6, fade=3),
            f'execute {plant} positioned ~ {CY} ~ run ' + g.card('ring', '^ ^0.1 ^', rot='~ 90', s0=0.8, s1=6.4, life=9, fade=4),
            f'execute {plant} positioned ~ {CY} ~ run ' + g.dust(A.GOLD_PALE, 1.6, '^ ^1.5 ^', (0.15, 1.6, 0.15), 24),
            f'execute {plant} positioned ~ {CY} ~ run ' + g.particle('block{block_state:"minecraft:gold_block"}', '^ ^0.3 ^', (1.4, 0.2, 1.4), 0, 24)]
            + [f'execute {plant} positioned ~ {CY} ~ rotated ~{a} 0 run ' + g.card('shard', '^ ^ ^1.4', rot=f'~ -{25 + (a // 45) % 2 * 15}', s0=0.2, s1=1.1, life=12, fade=5)
               for a in range(0, 360, 45)]
            + [f'execute {plant} run ' + g.sound('entity.generic.explode', 0.8, 0.9),
               f'execute {plant} run ' + g.sound('block.amethyst_cluster.break', 1.0, 0.8),
               f'execute {plant} run ' + g.sound('item.trident.thunder', 0.3, 1.2),
               F('voice/start')])
        self.w('intro/pullout', [g.sound('block.chain.break', 0.8, 0.6), g.sound('block.stone.break', 0.8, 0.8),
                                 f'execute {plant} run ' + g.particle('block{block_state:"minecraft:gold_block"}', f'~ {CY + 0.2} ~', (0.3, 0.1, 0.3), 0, 10)])
        self.w('intro/done', [
            '# End of the untargetable intro; the entrance clip finishes its twirl to idle on its own.',
            'function rlk:mboss/intro_end',
            sc_set('#gdCool', 20),
            F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def ai(self):
        F, R, g = self.F, self.R, self.g
        self.w('ai/state', ['# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).'] + [
            f'execute if score #gdSt mb matches {ST[k]} run return run {F(fn)}'
            for k, fn in (('idle', 'ai/idle'), ('close', 'ai/close'), ('guard', 'guard/tick'), ('chaos', 'chaos/tick'),
                          ('groggy', 'groggy/tick'), ('approach', 'ai/approach'))])
        self.w('ai/enter', [
            '# Enter idle (#gdCool set by the caller).',
            sc_set('#gdSt', ST['idle']), sc_set('#gdT', 0), sc_set('#gdMv', 0),
            F('hud/sub_idle')])
        self.w('ai/idle', [
            '# @s = body. Hover and track the player; glide closer while farther than 9 b (she never walks);',
            '# decide when the cooldown is over.',
            R('face/track'),
            'execute if score #gdCool mb matches 1.. run scoreboard players remove #gdCool mb 1',
            f'execute unless entity @e[tag=rlk_body,distance=..9,limit=1] run {F("ai/drift")}',
            f'execute if score #gdMv mb matches 1 if entity @e[tag=rlk_body,distance=..8,limit=1] run {F("ai/hover")}',
            f'execute if score #gdCool mb matches ..0 run {F("ai/next")}'])
        self.w('ai/drift', [f'execute if score #gdMv mb matches 0 run {g.play("glide")}', sc_set('#gdMv', 1),
                            'function rlk:mboss/mv/toward {d:0.12}'])
        self.w('ai/hover', [g.play('idle'), sc_set('#gdMv', 0)])
        self.w('ai/next', [
            '# Next action. Test request > test lock (#mbLock 1-5 = that pattern only, 6 = guard pair + chaos only) >',
            '# rotation: #gdLeft normal patterns, then guard I, guard II, chaos (K3).',
            f'execute if score #gdMv mb matches 1 run {g.play("idle")}',
            sc_set('#gdMv', 0),
            f'execute if score #gdReq mb matches 1.. run return run {F("ai/req")}',
            f'execute if score #mbLock mb matches 1..5 run return run {F("ai/lock")}',
            f'execute if score #mbLock mb matches 6 run return run {F("guard/begin1")}',
            f'execute if score #gdLeft mb matches ..0 run return run {F("guard/begin1")}',
            'scoreboard players remove #gdLeft mb 1',
            F('ai/pick')])
        self.w('ai/req', ['scoreboard players operation #gdPick mb = #gdReq mb', sc_set('#gdReq', 0), F('ai/launch')])
        self.w('ai/lock', ['scoreboard players operation #gdPick mb = #mbLock mb', F('ai/launch')])
        # shuffle bag
        bands = A.BANDS
        cand = ['# Candidates: in the bag, allowed in the current range band, not the last one.']
        cand_any = ['# Fallback candidates: allowed in the band (bag and last ignored).']
        for p in self.normal:
            cand.append(sc_set(f'#gdC{p.id}', 0))
            cand_any.append(sc_set(f'#gdC{p.id}', 0))
            for b in p.bands:
                cand.append(f'execute if score #gdBag{p.id} mb matches 1 if score #gdBand mb matches {bands[b]} '
                            f'unless score #gdLast mb matches {p.id} run scoreboard players set #gdC{p.id} mb 1')
                cand_any.append(f'execute if score #gdBand mb matches {bands[b]} run scoreboard players set #gdC{p.id} mb 1')
        for lines in (cand, cand_any):
            lines.append(sc_set('#gdCn', 0))
            lines += [f'execute if score #gdC{p.id} mb matches 1 run scoreboard players add #gdCn mb 1' for p in self.normal]
        self.w('ai/cand', cand)
        self.w('ai/cand_any', cand_any)
        self.w('ai/refill', ['# The bag ran dry for this band: refill it with every normal pattern.']
               + [sc_set(f'#gdBag{p.id}', 1) for p in self.normal])
        draw = ['# #gdR = 0..#gdCn-1 -> the #gdR-th candidate.', sc_set('#gdPick', 0)]
        for p in self.normal:
            draw.append(f'execute if score #gdPick mb matches 0 if score #gdC{p.id} mb matches 1 if score #gdR mb matches 0 '
                        f'run scoreboard players set #gdPick mb {p.id}')
            draw.append(f'execute if score #gdC{p.id} mb matches 1 run scoreboard players remove #gdR mb 1')
        draw += [f'execute if score #gdPick mb matches {p.id} run scoreboard players set #gdBag{p.id} mb 0' for p in self.normal]
        self.w('ai/draw', draw)
        mel, far = int(A.MELEE * 10), int(A.FAR * 10)
        self.w('ai/pick', [
            '# @s = body. Range-filtered shuffle bag with no immediate repeat (K2/K3):',
            '# ' + ', '.join(f'P{p.id} {"/".join(p.bands)}' for p in self.normal) + f' (melee <= {A.MELEE} b, far >= {A.FAR} b).',
            'function rlk:mboss/mv/dist',
            'scoreboard players operation #gdDist mb = #mbDist mb',
            sc_set('#gdBand', bands['mid']),
            f'execute if score #gdDist mb matches ..{mel} run scoreboard players set #gdBand mb {bands["melee"]}',
            f'execute if score #gdDist mb matches {far}.. run scoreboard players set #gdBand mb {bands["far"]}',
            F('ai/cand'),
            f'execute if score #gdCn mb matches 0 run {F("ai/refill")}',
            f'execute if score #gdCn mb matches 0 run {F("ai/cand")}',
            f'execute if score #gdCn mb matches 0 run {F("ai/cand_any")}',
            'execute if score #gdCn mb matches 0 run scoreboard players set #gdC1 mb 1',
            'execute if score #gdCn mb matches 0 run scoreboard players set #gdCn mb 1',
            'execute store result score #gdR mb run random value 0..999',
            'scoreboard players operation #gdR mb %= #gdCn mb',
            F('ai/draw'),
            'execute if score #gdPick mb matches 0 run scoreboard players set #gdPick mb 1',
            'scoreboard players operation #gdLast mb = #gdPick mb',
            F('ai/launch')])
        launch = ['# #gdPick = pattern id: start it, melee patterns close in first.']
        close = ['# @s = body, closing in for #gdPick (glide 0.3 b/t, at most 30 t), then the pattern starts.',
                 'scoreboard players add #gdT mb 1',
                 'function rlk:mboss/mv/turn {max:30}',
                 'function rlk:mboss/mv/toward {d:0.3}']
        for p in self.pats:
            if p.close:
                launch.append(f'execute if score #gdPick mb matches {p.id} unless entity @e[tag=rlk_body,distance=..{L.num(p.close)},limit=1] '
                              f'run return run {F("ai/close_begin")}')
                close.append(f'execute if score #gdPick mb matches {p.id} if entity @e[tag=rlk_body,distance=..{L.num(p.close)},limit=1] '
                             f'run return run {F("ai/go")}')
        launch.append(F('ai/go'))
        close.append(f'execute if score #gdT mb matches 30.. run {F("ai/go")}')
        self.w('ai/launch', launch)
        self.w('ai/close', close)
        self.w('ai/close_begin', [sc_set('#gdSt', ST['close']), sc_set('#gdT', 0), g.play('glide'), F('hud/sub_pattern')])
        self.w('ai/go', ['# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).',
                         sc_set('#gdSt', ST['pattern']), 'scoreboard players operation #gdPat mb = #gdPick mb',
                         sc_set('#gdPNew', 1)])
        self.w('ai/approach_begin', [
            '# After a failed chaos: she leaves the centre and glides at the player (patterns.md §9.4).',
            sc_set('#gdSt', ST['approach']), sc_set('#gdT', 0), g.play('glide'), F('hud/sub_idle')])
        self.w('ai/approach', [
            'scoreboard players add #gdT mb 1',
            R('face/track'),
            'function rlk:mboss/mv/toward {d:0.15}',
            f'execute if entity @e[tag=rlk_body,distance=..2.5,limit=1] run return run {F("ai/approach_end")}',
            f'execute if score #gdT mb matches 40.. run {F("ai/approach_end")}'])
        self.w('ai/approach_end', [g.play('idle'), sc_set('#gdCool', 14), F('ai/enter')])
        rec = ['# A slot pattern finished (#gdPDone = its id): recovery before the next decision.', sc_set('#gdCool', 20)]
        rec += [sc_set_if('#gdPDone', p.id, '#gdCool', p.recover) for p in self.pats]
        rec.append(F('ai/enter'))
        self.w('ai/recover', rec)
        self.w('ai/pat_done', [
            '# From p/finish: the state that owns the slot continues.',
            f'execute if score #gdSt mb matches {ST["guard"]} run return run {F("guard/after")}',
            f'execute if score #gdSt mb matches {ST["chaos"]} run return run scoreboard players set #gdFailDone mb 1',
            F('ai/recover')])

    # -----------------------------------------------------------------------------------------
    def slot(self):
        F = self.F
        begin = ['# @s = body. First tick of the slot pattern #gdPat: clock 0, start function (plays its clip).',
                 sc_set('#gdPNew', 0), sc_set('#gdPT', 0), sc_set('#gdPEnd', 0), sc_set('#gdPMax', 200)]
        begin += [sc_set_if('#gdPat', p.id, '#gdPMax', p.max_len) for p in self.pats]
        begin += [f'execute if score #gdSt mb matches {ST["pattern"]} run {F("hud/sub_pattern")}', F('p/start')]
        self.w('p/begin', begin)
        self.w('p/run', [
            '# @s = body. The slot: start on the tick it was picked, then tick with #gdPT = 1, 2, ... (= clip tick).',
            f'execute if score #gdPNew mb matches 1 run return run {F("p/begin")}',
            'scoreboard players add #gdPT mb 1',
            F('p/tick'),
            f'execute if score #gdPEnd mb matches 1 run return run {F("p/finish")}',
            f'execute if score #gdPT mb >= #gdPMax mb run {F("p/finish")}'])
        self.w('p/finish', [
            '# @s = body. The pattern ended (p/end or its max_len): clear the slot and tell the owning state.',
            'scoreboard players operation #gdPDone mb = #gdPat mb',
            sc_set('#gdPat', 0), sc_set('#gdPEnd', 0), sc_set('#gdPT', 0),
            f'execute unless score #gdSt mb matches {ST["chaos"]} run scoreboard players set #mbNoLeash mb 0',
            'tag @s remove rlk_mb_inv',
            F('ai/pat_done')])
        self.w('p/end', ['# Called by a pattern (any executor): it is done; the core finishes it after this tick\'s pattern tick.',
                         sc_set('#gdPEnd', 1)])
        self.w('p/cancel', [
            '# Stop the slot pattern now (tests, death, reload). Callers run rlk:mboss/lib_clear first when hazards must',
            '# go. The pattern\'s cancel runs as the caller (the body when it exists): it must use selectors, not @s.',
            f'execute if score #gdPat mb matches 1.. unless score #gdPNew mb matches 1 run {F("p/cancel_d")}',
            sc_set('#gdPat', 0), sc_set('#gdPNew', 0), sc_set('#gdPEnd', 0), sc_set('#gdPT', 0),
            sc_set('#mbNoLeash', 0),
            'execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv',
            f'execute if score #mbSt mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run {self.R("spear/geo")}'])
        for name, doc in (('start', 'start (clock 0)'), ('tick', 'tick (#gdPT 1..)'), ('cancel_d', 'cancel')):
            target = 'cancel' if name == 'cancel_d' else name
            self.w(f'p/{name}', [f'# GENERATED dispatcher: the running pattern\'s {doc}, by #gdPat.']
                   + [f'execute if score #gdPat mb matches {p.id} run return run {F(f"p/{p.key}/{target}")}' for p in self.pats])
        self.w('p/pause_d', ['# GENERATED dispatcher: the running pattern\'s optional pause (the fight just froze: player dead or',
                             '# reviving), by #gdPat. Not for a pattern picked this tick (its start has not run yet).',
                             'execute unless score #gdPat mb matches 1.. run return 0',
                             'execute if score #gdPNew mb matches 1 run return 0']
               + [f'execute if score #gdPat mb matches {p.id} run return run {F(f"p/{p.key}/pause")}'
                  for p in self.pats if self.g.has(f'p/{p.key}/pause')])
        vis = ['# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.',
               'scoreboard players operation #gdV mb = @s mbHzV', 'scoreboard players operation #gdV mb /= #c10 mb']
        vis += [f'execute if score #gdV mb matches {p.id} run return run {F(f"p/{p.key}/vis")}'
                for p in self.pats if self.g.has(f'p/{p.key}/vis')]
        self.w('p/vis', vis)
        pj = ['# GENERATED: pj_end of props whose mbId = pattern id (@s = prop; #pjEv, #pjKeep preset).']
        pj += [f'execute if score @s mbId matches {p.id} run return run {F(f"p/{p.key}/pj_end")}'
               for p in self.pats if self.g.has(f'p/{p.key}/pj_end')]
        self.w('p/pj_end', pj)

    # -----------------------------------------------------------------------------------------
    def guard(self):
        F, R, g = self.F, self.R, self.g
        self.w('guard/begin1', [sc_set('#gdGN', 1), F('guard/begin')])
        self.w('guard/begin2', [sc_set('#gdGN', 2), F('guard/begin')])
        begin = [
            '# @s = body. Guard mode #gdGN (1 = slot A, 2 = slot B): entry twirl (50 t), then 100 t of record window.',
            sc_set('#gdSt', ST['guard']), sc_set('#gdT', 0), sc_set('#gdGP', 1),
            sc_set('#gdRecOn', 0), sc_set('#gdRecNew', 0), sc_set('#gdRecEl', 0)]
        for e in range(1, 5):
            begin += [sc_set(f'#gdN{e}', 0), sc_set(f'#gdQ{e}', REC_NEW), sc_set(f'#gdRc{e}', 0),
                      f'execute if score #gdGN mb matches 2 if score #gdSlotA mb matches {e} run scoreboard players set #gdQ{e} mb {REC_AGAIN}']
        begin += [R('face/player'), g.play('guard_entry'),
                  F('look/eye_guard'),
                  F('voice/guard'),
                  g.sound('item.trident.riptide_1', 0.7, 0.8), g.sound('entity.player.attack.sweep', 0.6, 0.6),
                  F('hud/sub_guard')]
        self.w('guard/begin', begin)
        self.w('guard/tick', [
            'scoreboard players add #gdT mb 1',
            f'execute if score #gdGP mb matches 1 run return run {F("guard/entry")}',
            f'execute if score #gdGP mb matches 2 run return run {F("guard/active")}',
            f'execute if score #gdGP mb matches 4 run return run {F("guard/gap")}',
            '# phase 3: the sweep pattern runs in the slot (guard/after when it ends)'])
        disc = lambda t, pos, rot: at_t('#gdT', t, g.card('ring', pos, rot=rot, spin=140, s0=0.5, s1=3.4, life=10, fade=4))
        self.w('guard/entry', [
            '# @s = body, guard clock 1..50: baton twirl, vertical spin discs (16-35), gold ground ring (35), settle.',
            '# Discs and ring are telegraphs only (no damage, K24).',
            R('face/track'),
            at_t('#gdT', 6, g.sound('item.trident.riptide_1', 0.6, 0.9)),
            at_t('#gdT', 11, g.sound('entity.player.attack.sweep', 0.6, 0.7)),
            disc(16, '^-1.3 ^1.6 ^0.2', '~90 0'),
            disc(22, '^ ^1.6 ^1.4', '~ 0'),
            disc(28, '^1.1 ^1.6 ^1.0', '~-45 0'),
            at_t('#gdT', 16, g.sound('item.trident.throw', 0.6, 1.0)),
            at_t('#gdT', 16, g.sound('block.amethyst_block.chime', 0.9, 1.6)),
            at_t('#gdT', 22, g.sound('block.amethyst_block.chime', 0.9, 1.8)),
            at_t('#gdT', 28, g.sound('entity.illusioner.cast_spell', 0.4, 1.4)),
            at_t('#gdT', (28, 35), g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.2 ~', (1.2, 0.1, 1.2), 0, 3)),
            at_t('#gdT', 35, g.card('ring', '~ ~0.1 ~', rot='~ 90', s0=1.0, s1=9.4, life=9, fade=4)),
            at_t('#gdT', 35, g.sound('block.amethyst_block.place', 1.0, 0.5)),
            at_t('#gdT', 35, g.sound('entity.iron_golem.step', 0.8, 0.6)),
            at_t('#gdT', (36, 44), g.dust(A.GOLD, 1.0, '~ ~0.15 ~', (2.4, 0.02, 2.4), 6)),
            f'execute if score #gdT mb matches {GUARD_ENTRY}.. run {F("guard/open")}'])
        self.w('guard/open', ['# The record window opens (guard pose loop follows the entry clip on its own).',
                              sc_set('#gdGP', 2), sc_set('#gdRecOn', 1), g.sound('block.beacon.activate', 0.4, 1.6)])
        self.w('guard/active', [
            f'# @s = body, guard clock {GUARD_ENTRY + 1}..{GUARD_END}: gold aura, drift ~1 b/s toward the player, record window.',
            R('face/track'),
            'execute unless entity @e[tag=rlk_body,distance=..2.2,limit=1] run function rlk:mboss/mv/toward {d:0.05}',
            'scoreboard players operation #gdM mb = #gdT mb', 'scoreboard players operation #gdM mb %= #gdK3 mb',
            f'execute if score #gdM mb matches 0 run {g.dust(A.GOLD, 0.9, "~ ~1.9 ~", (0.55, 1.0, 0.55), 3)}',
            f'execute if score #gdM mb matches 0 run {g.particle("wax_on", "~ ~1.6 ~", (0.8, 1.2, 0.8), 0, 1)}',
            at_t('#gdT', (GUARD_END - 11, GUARD_END), g.dust(A.GOLD_PALE, 1.3, '~ ~2 ~', (0.45, 0.9, 0.45), 4)),
            at_t('#gdT', GUARD_END - 4, 'execute rotated as @s rotated ~ 0 run ' + g.card('star', '^ ^2.4 ^0.5', bb='center', spin=60, s0=0.4, s1=3.2, life=8, fade=4)),
            at_t('#gdT', GUARD_END - 4, g.sound('block.beacon.power_select', 0.6, 1.6)),
            f'execute if score #gdRecNew mb matches 1.. run return run {F("guard/record")}',
            f'execute if score #gdT mb matches {GUARD_END}.. run {F("guard/timeout")}'])
        self.w('guard/record', [
            '# A record completed (#gdRecNew = element): slot = element, enchanted spear (rig API), enchanted sweep',
            '# (pattern 12, p56) at once: its blade slices strike 21-27 t later (front at 23; patterns.md §8.2).',
            sc_set('#gdRecOn', 0),
            'scoreboard players operation #gdRecEl mb = #gdRecNew mb', sc_set('#gdRecNew', 0),
            'execute if score #gdGN mb matches 1 run scoreboard players operation #gdSlotA mb = #gdRecEl mb',
            'execute if score #gdGN mb matches 2 run scoreboard players operation #gdSlotB mb = #gdRecEl mb',
            'scoreboard players operation #gdSwEl mb = #gdRecEl mb',
            F('fx/record'),
            F('look/spear_rec'), F('look/eye_rec'),
            sc_set('#gdGP', 3), sc_set('#gdPat', 12), sc_set('#gdPNew', 1),
            F('hud/sub_guard')])
        self.w('guard/timeout', [
            f'# No record in {GUARD_ACTIVE} t: the gold sweep (pattern 11, p56); its blade slices strike 20-24 t later (front at 22).',
            sc_set('#gdRecOn', 0), sc_set('#gdGP', 3), sc_set('#gdPat', 11), sc_set('#gdPNew', 1)])
        self.w('guard/after', [
            '# From ai/pat_done: the sweep is over. Spear back to gold, the gems keep the latest recorded element.',
            R('spear/geo'), F('look/eye_rest'),
            sc_set('#gdGP', 4), sc_set('#gdT', 0),
            sc_set('#gdGW', GUARD_GAP[1]),
            f'execute if score #gdGN mb matches 2 run scoreboard players set #gdGW mb {GUARD_GAP[2]}',
            F('hud/sub_guard')])
        self.w('guard/gap', [
            '# Short reposition, then guard II (after guard I) or chaos (after guard II).',
            R('face/track'),
            'execute if score #gdT mb < #gdGW mb run return 0',
            f'execute if score #gdGN mb matches 1 run return run {F("guard/begin2")}',
            F('chaos/begin')])
        # record fx per element
        fx = ['# @s = body: record complete, a starburst in the element colour on her (patterns.md §8.2).']
        for e in range(1, 5):
            fx.append(f'execute if score #gdRecEl mb matches {e} run {g.dust(A.EL_RGB[e], 1.6, "~ ~2.2 ~", (0.5, 0.5, 0.5), 30)}')
        fx += [g.card('burst', '~ ~2.2 ~', bb='center', spin=30, s0=0.5, s1=2.4, life=5, fade=2),
               g.sound('entity.lightning_bolt.impact', 0.35, 1.5), g.sound('block.respawn_anchor.charge', 0.7, 1.2)]
        self.w('fx/record', fx)

    # -----------------------------------------------------------------------------------------
    def chaos(self):
        F, R, g = self.F, self.R, self.g
        near = L.num(CHAOS_NEAR)
        red_blk = 'block{block_state:"minecraft:red_concrete"}'
        leap_land = ev('chaos_leap', 'land')
        charge = clip_len('chaos_charge')
        self.w('chaos/begin', [
            '# @s = body. Chaos (K10): leap + arcing flight to the centre (from >= 6 b), else a short glide; landing;',
            '# charge with the spear level; rise to the hover; then the 350 t timer and the two stars.',
            sc_set('#gdSt', ST['chaos']), sc_set('#gdT', 0), sc_set('#gdCP', 1),
            sc_set('#mbNoLeash', 1), sc_set('#gdBrk', 0), sc_set('#gdFailDone', 0), sc_set('#gdStars', 0),
            R('eye/red'),
            sc_set('#gdChV', 1),
            f'execute if entity @e[tag=rlk_mb_arena,distance=..{near},limit=1] run scoreboard players set #gdChV mb 2',
            'execute if score #gdChV mb matches 1 at @s facing entity @e[tag=rlk_mb_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0',
            f'execute if score #gdChV mb matches 1 run {g.play("chaos_leap")}',
            f'execute if score #gdChV mb matches 1 run {g.sound("entity.phantom.flap", 0.8, 0.9)}',
            f'execute if score #gdChV mb matches 1 run {g.sound("item.elytra.flying", 0.4, 1.3)}',
            'execute if score #gdChV mb matches 1 run ' + g.particle(red_blk, '~ ~1 ~', (0.6, 0.6, 0.6), 0, 16),
            f'execute if score #gdChV mb matches 2 run {g.play("glide")}',
            f'execute if score #gdChV mb matches 2 run {g.sound("item.trident.riptide_1", 0.6, 0.6)}',
            F('hud/sub_chaos_in')])
        self.w('chaos/tick', [
            'scoreboard players add #gdT mb 1',
            f'execute if score #gdCP mb matches 1 run return run {F("chaos/travel")}',
            f'execute if score #gdCP mb matches 2 run return run {F("chaos/charge")}',
            f'execute if score #gdCP mb matches 3 run return run {F("chaos/hold")}',
            f'execute if score #gdCP mb matches 4 run return run {F("chaos/fail")}'])
        self.w('chaos/travel', [
            f'# Leap variant: chaos_leap (leap 0-9, flight 9-31, land {leap_land}); the body glides to the centre meanwhile.',
            '# Glide variant: 12 t glide, then chaos_charge.',
            f'execute if score #gdChV mb matches 1 if score #gdT mb matches 10 at @e[tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide {{t:{leap_land - 10}}}',
            f'execute if score #gdChV mb matches 1 if score #gdT mb matches 2..{leap_land - 1} run {g.dust_fade(A.RED_EDGE, A.CRIMSON_DARK, 1.5, "~ ~2.5 ~", (0.4, 0.6, 0.4), 3)}',
            f'execute if score #gdChV mb matches 1 if score #gdT mb matches {leap_land}.. run return run {F("chaos/land")}',
            'execute if score #gdChV mb matches 2 if score #gdT mb matches 1 at @e[tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide {t:12}',
            f'execute if score #gdChV mb matches 2 if score #gdT mb matches 12.. run {g.play("chaos_charge")}',
            f'execute if score #gdChV mb matches 2 if score #gdT mb matches 12.. run {F("chaos/land")}'])
        self.w('chaos/land', [
            '# On the centre star: landing (the heaviest boom of the fight for the leap), facing the player.',
            sc_set('#gdCP', 2), 'scoreboard players operation #gdCh0 mb = #gdT mb',
            R('face/player'),
            f'execute if score #gdChV mb matches 1 run {g.sound("entity.generic.explode", 0.6, 0.6)}',
            f'execute if score #gdChV mb matches 1 run {g.sound("block.anvil.land", 0.5, 0.5)}',
            f'execute if score #gdChV mb matches 1 run {g.card("ring", "~ ~0.1 ~", rot="~ 90", s0=1.0, s1=7.0, life=8, fade=3)}',
            'execute if score #gdChV mb matches 1 run ' + g.particle(red_blk, '~ ~0.3 ~', (1.6, 0.2, 1.6), 0, 30),
            f'execute if score #gdChV mb matches 2 run {g.sound("block.respawn_anchor.charge", 0.6, 1.0)}',
            g.sound('block.respawn_anchor.charge', 0.6, 1.5)])
        self.w('chaos/charge', [
            f'# @s = body, charge clock c = #gdT - #gdCh0: flare 7, red orb 16-30, rise 30, hover {charge} -> timer and stars.',
            'scoreboard players operation #gdCc mb = #gdT mb', 'scoreboard players operation #gdCc mb -= #gdCh0 mb',
            at_t('#gdCc', 7, 'execute rotated as @s rotated ~ 0 run ' + g.dust((1.0, 0.45, 0.25), 1.4, '^-0.4 ^2.3 ^1.6', (0.2, 0.2, 0.2), 14)),
            at_t('#gdCc', 7, g.sound('block.beacon.ambient', 0.8, 1.5)),
            at_t('#gdCc', (16, 30), 'execute rotated as @s rotated ~ 0 run ' + g.dust((0.89, 0.35, 0.32), 1.7, '^ ^2.4 ^0.6', (0.25, 0.25, 0.25), 3)),
            at_t('#gdCc', (16, 30), 'execute rotated as @s rotated ~ 0 run ' + g.particle('reverse_portal', '^ ^2.4 ^0.6', (0.4, 0.4, 0.4), 0.02, 2)),
            at_t('#gdCc', 30, g.sound('item.trident.riptide_2', 0.6, 0.8)),
            f'execute if score #gdCc mb matches {charge}.. run {F("chaos/hold_start")}'])
        self.w('chaos/hold_start', [
            '# @s = body hovering 3 b up (rig): the 350 t timer, two stars from slots A/B, the cross sigil, haze, streams.',
            sc_set('#gdCP', 3), sc_set('#gdTim', CHAOS_TIMER), sc_set('#gdTimS', CHAOS_TIMER // 20),
            sc_set('#gdHaze', 1), sc_set('#gdCsT', 16),
            R('face/player'),
            F('star/spawn_a'), F('star/spawn_b'),
            F('chaos/sigil'),
            g.sound('block.amethyst_cluster.break', 1.0, 1.2), g.sound('block.amethyst_block.resonate', 1.0, 1.4),
            g.sound('block.beacon.activate', 0.7, 1.4),
            F('hud/sub_chaos')])
        self.w('chaos/hold', [
            '# @s = body: timer, haze, cube streams (ambient, no damage, K11).',
            'scoreboard players remove #gdTim mb 1',
            'scoreboard players operation #gdTimS mb = #gdTim mb', 'scoreboard players add #gdTimS mb 19',
            'scoreboard players operation #gdTimS mb /= #gdK20 mb',
            f'execute if score #gdHaze mb matches 1 run {F("chaos/haze")}',
            'scoreboard players remove #gdCsT mb 1',
            f'execute if score #gdCsT mb matches ..0 run {F("chaos/cs_spawn")}',
            F('chaos/cs_all'),
            'scoreboard players operation #gdM mb = #gdT mb', 'scoreboard players operation #gdM mb %= #gdK8 mb',
            f'execute if score #gdM mb matches 0 run {g.dust(A.CRIMSON, 1.2, "~ ~6.7 ~", (0.4, 0.3, 0.4), 3)}',
            f'execute if score #gdTim mb matches ..0 run {F("chaos/fail_start")}'])
        # haze: 16 rim points, 4 per call, rotating
        haze = ['# Crimson haze (K21): dust columns at the arena rim and ash over the arena, every 4 t.',
                'scoreboard players operation #gdM mb = #gdT mb', 'scoreboard players operation #gdM mb %= #gdK4 mb',
                'execute unless score #gdM mb matches 0 run return 0',
                'scoreboard players operation #gdM mb = #gdT mb', 'scoreboard players operation #gdM mb /= #gdK4 mb',
                'scoreboard players operation #gdM mb %= #gdK4 mb']
        for k in range(4):
            haze.append(f'execute if score #gdM mb matches {k} run {F(f"chaos/haze{k}")}')
        haze.append(g.dust((0.59, 0.20, 0.27), 2.2, f'{CX} {CY + 7} {CZ}', (12, 4, 12), 6))
        self.w('chaos/haze', haze)
        for k in range(4):
            pts = []
            for j in range(4):
                a = math.radians((k + 4 * j) * 22.5 + 11.25)
                x, z = CX + 19.5 * math.sin(a), CZ + 19.5 * math.cos(a)
                pts.append(g.dust((0.62, 0.15, 0.24), 3.0, f'{L.num(x, 2)} {CY + 3} {L.num(z, 2)}', (1.2, 2.6, 1.2), 5))
                pts.append(g.dust((0.49, 0.15, 0.22), 2.0, f'{L.num(x, 2)} {CY + 7} {L.num(z, 2)}', (1.6, 2.0, 1.6), 3))
            self.w(f'chaos/haze{k}', pts)
        # cross sigil (5 cubes) above her head while hovering
        sig = ['# Red cross sigil above her head (patterns.md §9.2), billboarded upright; 5 cubes.']
        for (x, y, blk) in ((0, 0, 'redstone_block'), (0, 0.42, 'red_concrete'), (0, -0.42, 'red_concrete'),
                            (0.42, 0, 'red_concrete'), (-0.42, 0, 'red_concrete')):
            sig.append(f'summon minecraft:block_display ~ ~6.7 ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_fx","rlk_mb_gd_sigil"],'
                       f'billboard:"vertical",brightness:{{sky:15,block:15}},block_state:{{id:"minecraft:{blk}"}},view_range:2f,'
                       f'transformation:{{translation:[{L.num(x - 0.18, 3)}f,{L.num(y - 0.18, 3)}f,-0.18f],left_rotation:[0f,0f,0f,1f],'
                       f'right_rotation:[0f,0f,0f,1f],scale:[0.36f,0.36f,0.36f]}}}}')
        sig += [g.card('star', '~ ~6.7 ~', bb='center', spin=90, s0=0.2, s1=1.6, life=6, fade=3),
                g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~6.7 ~', (0.3, 0.3, 0.3), 0, 10)]
        self.w('chaos/sigil', sig)
        self.w('chaos/sigil_break', [
            'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_sigil] at @s run ' +
            g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~ ~', (0.15, 0.15, 0.15), 0, 4),
            'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_sigil]'])
        # cube streams
        self.w('chaos/cs_spawn', [
            '# @s = body: a new cube stream (at most 3) from around her, homing on the floor near the player.',
            'execute store result score #gdR mb run random value 18..30',
            'scoreboard players operation #gdCsT mb = #gdR mb',
            sc_set('#gdCsN', 0),
            'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs] run scoreboard players add #gdCsN mb 1',
            'execute if score #gdCsN mb matches 3.. run return 0',
            'summon minecraft:block_display ~ ~4.6 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_fx","rlk_mb_gd_cs","rlk_mb_gd_csnew"],'
            'brightness:{sky:15,block:15},block_state:{id:"minecraft:gold_block"},teleport_duration:1,view_range:2f,'
            'transformation:{translation:[-0.22f,-0.22f,-0.22f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.44f,0.44f,0.44f]}}',
            'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
            'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] run data modify entity @s Rotation[1] set value -35.0f',
            'scoreboard players set @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] mbT 0',
            'execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew,limit=1] store result score @s mbS run random value 1..2',
            'tag @e[type=minecraft:block_display,tag=rlk_mb_gd_csnew] remove rlk_mb_gd_csnew',
            g.sound('entity.blaze.shoot', 0.25, 0.6)])
        self.w('chaos/cs_all', ['execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_cs] at @s run ' + F('chaos/cs_tick')])
        self.w('chaos/cs_tick', [
            '# @s = stream head (gold cube): out along its own heading for 10 t, then a spiralling dive at the player\'s feet.',
            'scoreboard players add @s mbT 1',
            f'execute if score @s mbT matches 48.. run return run {F("chaos/cs_end")}',
            'execute if score @s mbT matches 10.. at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ ~',
            'execute if score @s mbS matches 1 at @s run tp @s ^0.2 ^ ^0.45',
            'execute if score @s mbS matches 2 at @s run tp @s ^-0.2 ^ ^0.45',
            g.dust_fade(A.RED_EDGE, (0.30, 0.15, 0.13), 1.5, '~ ~ ~', (0.06, 0.06, 0.06), 2),
            'scoreboard players operation #gdM mb = @s mbT', 'scoreboard players operation #gdM mb %= #gdK5 mb',
            f'execute if score #gdM mb matches 0 run {g.particle("small_flame", "~ ~ ~", (0.1, 0.1, 0.1), 0.01, 1)}',
            f'execute if score @s mbT matches 12.. at @s if entity @e[tag=rlk_body,distance=..1.4,limit=1] run return run {F("chaos/cs_end")}',
            f'execute at @s unless block ~ ~-0.3 ~ #rlk:cm_pass run {F("chaos/cs_end")}'])
        self.w('chaos/cs_end', [g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~ ~', (0.2, 0.2, 0.2), 0, 6),
                                g.sound('block.chain.place', 0.3, 1.4), 'kill @s'])
        # fail
        fail_land = 33
        fail_raise = 74
        self.w('chaos/fail_start', [
            '# T0 = the timer ran out (patterns.md §9.4). One fail spear per surviving star (pattern 13, p56): kinds in',
            '# #gdFailK1/#gdFailK2 (slot order), count in #gdFailN; the body clips and the ambience stay here.',
            sc_set('#gdCP', 4), sc_set('#gdF', 0), sc_set('#gdTim', 0), sc_set('#gdTimS', 0),
            sc_set('#gdFailN', 0), sc_set('#gdFailK1', 0), sc_set('#gdFailK2', 0), sc_set('#gdFailDone', 0),
            'execute if score #gdSa1 mb matches 1 run scoreboard players add #gdFailN mb 1',
            'execute if score #gdSa1 mb matches 1 run scoreboard players operation #gdFailK1 mb = #gdSk1 mb',
            'execute if score #gdSa2 mb matches 1 run scoreboard players add #gdFailN mb 1',
            'execute if score #gdSa2 mb matches 1 if score #gdFailN mb matches 1 run scoreboard players operation #gdFailK1 mb = #gdSk2 mb',
            'execute if score #gdSa2 mb matches 1 if score #gdFailN mb matches 2 run scoreboard players operation #gdFailK2 mb = #gdSk2 mb',
            g.play('chaos_fail'),
            g.sound('block.respawn_anchor.deplete', 0.9, 0.7), g.sound('block.bell.resonate', 0.3, 0.8),
            f'execute if score #gdFailN mb matches 1.. run scoreboard players set #gdPat mb 13',
            f'execute if score #gdFailN mb matches 1.. run scoreboard players set #gdPNew mb 1',
            'execute if score #gdFailN mb matches 0 run scoreboard players set #gdFailDone mb 1',
            F('hud/sub_fail')])
        self.w('chaos/fail', [
            f'# @s = body, fail clock F = 1..: stars flash 7 and collapse, streams stop 12, sigil breaks 15 + absorption,',
            f'# red ring 18, chest starburst 19, smoke + haze off 21, chaos_land {fail_land}, chaos_raise {fail_raise} (2 spears).',
            'scoreboard players add #gdF mb 1',
            at_t('#gdF', (1, 11), F('chaos/cs_all')),
            at_t('#gdF', 7, F('star/flash')),
            at_t('#gdF', 9, F('star/shrink')),
            at_t('#gdF', (10, 14), 'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] at @s run '
                 + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~1.2 ~', (0.25, 0.25, 0.25), 0, 2)),
            at_t('#gdF', 12, 'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs]'),
            at_t('#gdF', 15, F('chaos/sigil_break')),
            at_t('#gdF', 15, F('star/absorb')),
            at_t('#gdF', 15, g.sound('block.beacon.activate', 0.8, 1.6)),
            at_t('#gdF', 15, g.sound('entity.evoker.cast_spell', 0.6, 1.0)),
            at_t('#gdF', 16, g.sound('entity.wither.shoot', 0.3, 0.5)),
            at_t('#gdF', 18, F('fx/red_ring')),
            at_t('#gdF', 19, g.card('burst', '~ ~6.2 ~', bb='center', spin=30, s0=0.6, s1=4.0, life=6, fade=3)),
            at_t('#gdF', 21, g.particle('large_smoke', '~ ~5.5 ~', (1.6, 0.8, 1.6), 0.02, 30)),
            at_t('#gdF', 21, sc_set('#gdHaze', 0)),
            at_t('#gdF', fail_land, g.play('chaos_land')),
            at_t('#gdF', fail_land + ev('chaos_land', 'land'), g.sound('block.amethyst_block.fall', 0.8, 0.7)),
            f'execute if score #gdF mb matches {fail_raise} if score #gdFailN mb matches 2.. run {g.play("chaos_raise")}',
            f'execute if score #gdF mb matches {fail_land + ev("chaos_land", "land")}.. if score #gdFailDone mb matches 1 run return run {F("chaos/fail_end")}',
            f'execute if score #gdF mb matches 170.. run {F("chaos/fail_end")}'])
        self.w('chaos/fail_end', [
            '# Spears done and she is on the floor: slots reset (K22), then the approach and 4-5 normal patterns.',
            f'execute if score #gdPat mb matches 1.. run {F("p/cancel")}',
            F('chaos/reset'),
            f'execute store result score #gdLeft mb run random value {NEXT_AFTER_CHAOS[0]}..{NEXT_AFTER_CHAOS[1]}',
            F('ai/approach_begin')])
        self.w('chaos/success', [
            '# @s = body: the second star broke inside the timer -> groggy (the 18 % hit lands 5 t later via star/bq2).',
            sc_set('#gdTim', 0), sc_set('#gdTimS', 0), sc_set('#gdHaze', 0),
            F('chaos/sigil_break'),
            'kill @e[type=minecraft:block_display,tag=rlk_mb_gd_cs]',
            g.play('chaos_fall'),
            F('groggy/begin')])
        self.w('chaos/reset', [
            '# End of a chaos cycle (groggy end, fail end, death, tests, reload): stars, sigil, streams, haze gone;',
            '# both record slots reset (K22) and the looks back to gold.',
            'kill @e[type=minecraft:husk,tag=rlk_mb_gd_star]',
            'kill @e[tag=rlk_mb_gd_fx]',
            sc_set('#gdStars', 0), sc_set('#gdSa1', 0), sc_set('#gdSa2', 0), sc_set('#gdCP', 0), sc_set('#gdTim', 0),
            sc_set('#gdTimS', 0), sc_set('#gdHaze', 0), sc_set('#gdBrk', 0), sc_set('#gdFailDone', 0),
            sc_set('#gdSlotA', 0), sc_set('#gdSlotB', 0),
            sc_set('#mbNoLeash', 0),
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run {R("eye/geo")}',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run {R("spear/geo")}'])
        ring = ['# Red gyroscope ring around her upper body (fail +18).']
        for a in range(0, 360, 30):
            ring.append(f'execute rotated {a} 0 run ' + g.dust((0.70, 0.04, 0.18), 1.5, '^ ^5.4 ^1.9', (0, 0.05, 0), 2))
        self.w('fx/red_ring', ring)

    # -----------------------------------------------------------------------------------------
    def stars(self):
        F, g = self.F, self.g
        for slot, (lab, ang, inert) in {1: ('A', STAR_ANGLE, 5), 2: ('B', -STAR_ANGLE, 6)}.items():
            sl = '#gdSlotA' if slot == 1 else '#gdSlotB'
            side = "her right, the player's left" if slot == 1 else "her left, the player's right"
            self.w(f'star/spawn_{lab.lower()}', [
                f'# @s = body: star of slot {lab} ({side}),'
                f' {L.num(STAR_DIST)} b out. Kind = the recorded element (active) or {inert} (inert {A.STAR_KO[inert]}).',
                f'scoreboard players operation #gdSk{slot} mb = {sl} mb',
                f'execute if score #gdSk{slot} mb matches 0 run scoreboard players set #gdSk{slot} mb {inert}',
                f'scoreboard players operation #gdSk mb = #gdSk{slot} mb',
                sc_set('#gdSs', slot), sc_set(f'#gdSa{slot}', 1),
                f'execute rotated as @s rotated ~{ang} 0 positioned ^ ^ ^{L.num(STAR_DIST)} positioned ~ {CY} ~ run {F("star/make")}'])
        self.w('star/make', [
            '# At the star spot (floor): aux husk with its own pool (per mille of the body max HP), RES and kind, plus the',
            '# glyph visual. #gdSk = kind (1-4 element, 5/6 inert), #gdSs = slot.',
            sc_set('#gdPm', STAR_PM['active']), sc_set('#auxRes', 0),
            f'execute if score #gdSk mb matches 5.. run scoreboard players set #gdPm mb {STAR_PM["inert"]}',
            f'execute if score #gdSk mb matches 5.. run scoreboard players set #auxRes mb {STAR_RES_INERT}',
            F('star/pool'),
            'function rlk:mboss/aux/spawn',
            'tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_gd_star',
            'scoreboard players operation @e[tag=rlk_mb_auxlast,limit=1] mbS = #gdSk mb',
            'scoreboard players operation @e[tag=rlk_mb_auxlast,limit=1] mbId = #gdSs mb',
            'scoreboard players set @e[tag=rlk_mb_auxlast,limit=1] mbT 0']
            + [f'execute if score #gdSk mb matches {k} run {F(f"star/vis{k}")}' for k in range(1, 7)]
            + ['scoreboard players operation @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew,limit=1] mbId = #gdSs mb',
               'scoreboard players set @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew,limit=1] mbT 0',
               'tag @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew] remove rlk_mb_gd_svnew',
               g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~0.6 ~', (0.3, 0.3, 0.3), 0, 8),
               'scoreboard players add #gdStars mb 1'])
        for k in range(1, 7):
            self.w(f'star/vis{k}', [
                f'# Star glyph, {A.STAR_KO[k]} ({A.STAR_HEX[k]}): a billboard 4-point star that grows from 0.',
                f'summon minecraft:text_display ~ ~1.3 ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_fx","rlk_mb_gd_starv","rlk_mb_gd_svnew"],'
                f'billboard:"center",background:0,shadow:true,see_through:false,brightness:{{sky:15,block:15}},alignment:"center",'
                f'text:{{text:"✦",color:"{A.STAR_HEX[k]}"}},view_range:2f,'
                f'transformation:{{translation:[0f,-0.4f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.2f,0.2f,0.2f]}}}}'])
        self.w('star/pool', [
            '# #auxHp = body max HP x #gdPm / 1000 (overflow-safe); #auxHpPct stays 0 so aux/spawn uses #auxHp.',
            'scoreboard players operation #gdX mb = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] mhpM',
            'execute if score #gdX mb matches 2000000.. run scoreboard players operation #gdX mb /= #c1000 mb',
            'execute if score #gdX mb matches 2000000.. run scoreboard players operation #gdX mb *= #gdPm mb',
            'execute if score #gdX mb matches ..1999999 run scoreboard players operation #gdX mb *= #gdPm mb',
            'execute if score #gdX mb matches ..1999999 run scoreboard players operation #gdX mb /= #c1000 mb',
            'execute if score #gdX mb matches ..0 run scoreboard players set #gdX mb 1',
            'scoreboard players operation #auxHp mb = #gdX mb', sc_set('#auxHpPct', 0)])
        aura = {1: 'aFire', 2: 'aWater', 3: 'aThunder', 4: 'aIce'}
        one = ['# @s = star husk, at @s: permanent aura of an active star ("기록 원소 상시 부착"), sparks, break check.',
               'scoreboard players add @s mbT 1']
        for k, obj in aura.items():
            one.append(f'execute if score @s mbS matches {k} run scoreboard players set @s {obj} 1000')
        one.append('execute if score @s mbS matches 1..4 run scoreboard players set @s elAct 1')
        one += ['scoreboard players operation #gdM mb = @s mbT', 'scoreboard players operation #gdM mb %= #gdK4 mb']
        sparks = {1: ('flame', 0.02), 2: ('falling_water', 0), 3: ('electric_spark', 0.05), 4: ('snowflake', 0.02),
                  5: ('wax_on', 0), 6: ('end_rod', 0.01)}
        for k, (pt, sp) in sparks.items():
            one.append(f'execute if score #gdM mb matches 0 if score @s mbS matches {k} run '
                       + g.particle(pt, '~ ~1.3 ~', (0.35, 0.45, 0.35), sp, 2))
        one.append(f'execute if entity @s[tag=rlk_mb_broken] run {F("star/broke")}')
        self.w('star/one', one)
        self.w('star/tick', [
            '# @s = body: every star husk, then the glyphs (growth over the timer).',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star] at @s run {F("star/one")}',
            f'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] run {F("star/vis_tick")}'])
        self.w('star/vis_tick', [
            '# @s = star glyph: voxel cluster -> crystal in 8 t, then slow growth to about 2 b over the timer (C9).',
            'scoreboard players add @s mbT 1',
            'execute if score @s mbT matches 2 run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:{translation:[0f,-0.6f,0f],scale:[5f,5f,5f]}}',
            f'execute if score @s mbT matches 12 run data merge entity @s {{start_interpolation:0,interpolation_duration:{CHAOS_TIMER - 12},transformation:{{translation:[0f,-1.0f,0f],scale:[8.5f,8.5f,8.5f]}}}}'])
        brk = ['# @s = a broken star husk (rlk_mb_broken from aux/take). 1st break -> 6 %, 2nd -> 18 % + groggy, each',
               f'# {BREAK_DELAY} t later (patterns.md §9.3). Number colour = the star colour.',
               'scoreboard players add #gdBrk mb 1',
               'scoreboard players remove #gdStars mb 1',
               'scoreboard players operation #gdX mb = @s mbS',
               'execute if score #gdX mb matches 5 run scoreboard players set #gdX mb 5',
               'execute if score #gdX mb matches 6 run scoreboard players set #gdX mb 2',
               f'execute if score #gdBrk mb matches 1 run scoreboard players set #gdBq1 mb {BREAK_DELAY + 1}',
               'execute if score #gdBrk mb matches 1 run scoreboard players operation #gdBe1 mb = #gdX mb',
               f'execute if score #gdBrk mb matches 2.. run scoreboard players set #gdBq2 mb {BREAK_DELAY + 1}',
               'execute if score #gdBrk mb matches 2.. run scoreboard players operation #gdBe2 mb = #gdX mb',
               'scoreboard players operation #gdX mb = @s mbId',
               'execute if score #gdX mb matches 1 run scoreboard players set #gdSa1 mb 0',
               'execute if score #gdX mb matches 2 run scoreboard players set #gdSa2 mb 0',
               'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] if score @s mbId = #gdX mb run kill @s']
        for k in range(1, 7):
            brk.append(f'execute if score @s mbS matches {k} run ' + g.dust(A.STAR_RGB[k], 1.8, '~ ~1.3 ~', (0.4, 0.5, 0.4), 30))
        brk += [g.particle('end_rod', '~ ~1.3 ~', (0.2, 0.3, 0.2), 0.12, 14),
                'execute if score #gdBrk mb matches 1 run ' + g.sound('block.amethyst_cluster.break', 1.0, 1.0),
                'execute if score #gdBrk mb matches 1 run ' + g.sound('block.respawn_anchor.deplete', 0.7, 1.2),
                'execute if score #gdBrk mb matches 2.. run ' + g.sound('block.amethyst_block.break', 1.0, 1.0),
                'execute if score #gdBrk mb matches 2.. run ' + g.sound('block.glass.break', 1.0, 1.4),
                'execute if score #gdBrk mb matches 2.. run ' + g.sound('entity.lightning_bolt.impact', 0.3, 2.0),
                f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("fx/star_hit")}',
                'kill @s',
                f'execute if score #gdBrk mb matches 2.. as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("chaos/success")}',
                f'execute if score #gdBrk mb matches 1 run {F("hud/sub_chaos")}']
        self.w('star/broke', brk)
        self.w('fx/star_hit', ['# @s = body: the break\'s starburst on her chest (S+1, hovering 3 b up).',
                               g.card('burst', '~ ~5.0 ~', bb='center', spin=24, s0=0.4, s1=2.2, life=5, fade=2),
                               g.particle('end_rod', '~ ~5 ~', (0.3, 0.3, 0.3), 0.08, 10)])
        for q, pct in ((1, BREAK_PCT[0]), (2, BREAK_PCT[1])):
            self.w(f'star/bq{q}', [
                f'# @s = body: queued punishment of break {q} ({pct} % of max HP as true damage, may be lethal).',
                f'scoreboard players remove #gdBq{q} mb 1',
                f'execute if score #gdBq{q} mb matches 1.. run return 0',
                f'scoreboard players operation #mbTrueEl mb = #gdBe{q} mb',
                f'execute rotated 0 0 run {F("fx/break_ring")}',
                f'function rlk:mboss/true_pct {{pct:{pct}}}'])
        ring = ['# Thin ring around her when a break punishment lands.']
        for a in range(0, 360, 30):
            ring.append(f'execute rotated {a} 0 run ' + g.dust(A.GOLD_PALE, 1.1, '^ ^4.8 ^1.2', (0, 0, 0), 1))
        self.w('fx/break_ring', ring + [g.sound('entity.generic.explode', 0.4, 1.6)])
        self.w('star/ignore', ['# Hit on a star outside a running chaos timer: nothing happens (no number, no pool change).',
                               'scoreboard players set #dmg tmp 0', 'scoreboard players set #mbAuxDone mb 1'])
        imm = ['# Own-element hit on an active star (C11).']
        if IMMUNE_PCT <= 0:
            imm.append('scoreboard players set #dmg tmp 0')
        else:
            imm += [f'scoreboard players set #gdX mb {IMMUNE_PCT}', 'scoreboard players operation #dmg tmp *= #gdX mb',
                    'scoreboard players operation #dmg tmp /= #c100 mb']
        self.w('star/immune', imm)
        self.w('star/flash', [
            '# Fail +7: stars flash white, their husks (and HP bars) go.',
            'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] run data merge entity @s {text:{text:"✦",color:"#FFFFFF"}}',
            'kill @e[type=minecraft:husk,tag=rlk_mb_gd_star]', sc_set('#gdStars', 0)])
        self.w('star/shrink', [
            'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] run data merge entity @s {text:{text:"✦",color:"#5A1418"},start_interpolation:0,interpolation_duration:5,transformation:{translation:[0f,-0.2f,0f],scale:[1.2f,1.2f,1.2f]}}'])
        self.w('star/absorb', [
            '# Fail +15: two cube chains fly from the stars into her chest; the glyphs go.',
            'execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run '
            + F('fx/absorb_line'),
            'kill @e[type=minecraft:text_display,tag=rlk_mb_gd_starv]'])
        self.w('fx/absorb_line', ['# From a star glyph (1.3 b up, 4.2 b out) to her chest (5 b up over the body), 8 points.']
               + [g.dust((0.99, 0.80, 0.33) if i % 3 == 0 else A.RED_EDGE, 1.3,
                         f'^ ^{L.num(3.7 * i / 8, 2)} ^{L.num(STAR_DIST * i / 8, 2)}', (0.05, 0.05, 0.05), 2) for i in range(1, 9)])

    # -----------------------------------------------------------------------------------------
    def groggy(self):
        F, g = self.F, self.g
        gb = 136
        self.w('groggy/begin', [
            f'# @s = body, after chaos_fall: {GROGGY} t without attacks (K13): fall 20, pose A to {gb}, pose B {gb}-170,',
            '# get-up 170-210, stance to 220. No damage bonus.',
            sc_set('#gdSt', ST['groggy']), sc_set('#gdT', 0), sc_set('#mbNoLeash', 0),
            F('hud/sub_groggy')])
        pool = ['# Crimson pool around her (ripples and a thin ring at about 5.4 b).',
                g.dust((0.74, 0.10, 0.15), 1.6, '~ ~0.12 ~', (1.4, 0.02, 1.4), 8)]
        for a in range(0, 360, 30):
            pool.append(f'execute rotated {a} 0 run ' + g.dust((0.56, 0.19, 0.21), 1.2, '^ ^0.12 ^5.4', (0, 0, 0), 1))
        self.w('fx/pool', pool)
        self.w('groggy/tick', [
            'scoreboard players add #gdT mb 1',
            at_t('#gdT', 8, F('voice/groggy')),
            at_t('#gdT', ev('chaos_fall', 'land'), g.sound('block.amethyst_block.fall', 0.9, 0.8)),
            at_t('#gdT', ev('chaos_fall', 'land'), g.sound('entity.player.attack.knockback', 0.4, 0.8)),
            'scoreboard players operation #gdM mb = #gdT mb', 'scoreboard players operation #gdM mb %= #gdK6 mb',
            f'execute if score #gdM mb matches 0 if score #gdT mb matches 20..{gb} run {F("fx/pool")}',
            at_t('#gdT', 24, g.sound('block.beacon.ambient', 0.5, 0.6)),
            at_t('#gdT', 84, g.sound('block.beacon.ambient', 0.5, 0.6)),
            at_t('#gdT', gb, g.play('groggy_b')),
            at_t('#gdT', gb + clip_len('groggy_b'), g.sound('entity.phantom.flap', 0.8, 0.7)),
            at_t('#gdT', gb + clip_len('groggy_b') + 3, g.sound('entity.phantom.flap', 0.8, 0.7)),
            at_t('#gdT', gb + clip_len('groggy_b'), g.sound('item.armor.equip_elytra', 0.8, 1.0)),
            f'execute if score #gdT mb matches {GROGGY}.. run {F("groggy/end")}'])
        self.w('groggy/end', [
            '# Groggy over: slots reset (K22), 4-5 normal patterns before the next guard pair.',
            F('chaos/reset'),
            f'execute store result score #gdLeft mb run random value {NEXT_AFTER_CHAOS[0]}..{NEXT_AFTER_CHAOS[1]}',
            sc_set('#gdCool', 20),
            F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def voice(self):
        g = self.g
        self.w('voice/attack', [
            f'# Attack line (K18): one of two, at most once per {VOICE_CD // 20} s. Patterns call it at their cast/release tick.',
            'execute if score #gdVoCd mb matches 1.. run return 0',
            sc_set('#gdVoCd', VOICE_CD),
            'execute store result score #gdR mb run random value 0..1',
            'execute if score #gdR mb matches 0 run ' + g.say('처결하노라!', A.LINE_HEX, 2, 30, 2),
            'execute if score #gdR mb matches 1 run ' + g.say('사라져라 마땅한 존재여!', A.LINE_HEX, 2, 34, 2)])
        self.w('voice/guard', [
            f'# Guard entry line; once per guard pair (cooldown {VOICE_GUARD_CD // 20} s).',
            'execute if score #gdVoG mb matches 1.. run return 0',
            sc_set('#gdVoG', VOICE_GUARD_CD),
            g.say('기록하여 판결할 지어다.', A.LINE_HEX, 2, 40, 1)])
        self.w('voice/start', [g.say('통찰하여, 나의 마음을 보아라.', A.LINE_HEX, 2, 50, 1)])
        self.w('voice/groggy', [g.say('나의 주인님이시여...!', A.LINE_HEX, 3, 50, 1)])
        self.w('voice/death', [g.say('시련은... 끝났다...', A.LINE_HEX, 3, 60, 1)])

    # -----------------------------------------------------------------------------------------
    def looks(self):
        R = self.R
        self.w('look/spear_rec', ['# Enchanted spear in the recorded element (#gdRecEl).']
               + [f'execute if score #gdRecEl mb matches {e} run {R("spear/" + k)}' for e, k in A.EL_KEY.items()])
        self.w('look/eye_rec', ['# Shield eye in the recorded element (#gdRecEl).']
               + [f'execute if score #gdRecEl mb matches {e} run {R("eye/" + k)}' for e, k in A.EL_KEY.items()])
        self.w('look/eye_guard', [
            '# Guard aura: gold eye, or slot A\'s element when guard II re-records a remembered element (m2 B10-B17).',
            R('eye/gold')] + [f'execute if score #gdGN mb matches 2 if score #gdSlotA mb matches {e} run {R("eye/" + k)}'
                              for e, k in A.EL_KEY.items()])
        rest = ['# Outside guard/chaos: the gems keep the latest recorded element of this cycle, else the painted Geo eye.',
                R('eye/geo')]
        rest += [f'execute if score #gdSlotA mb matches {e} run {R("eye/" + k)}' for e, k in A.EL_KEY.items()]
        rest += [f'execute if score #gdSlotB mb matches {e} run {R("eye/" + k)}' for e, k in A.EL_KEY.items()]
        self.w('look/eye_rest', rest)

    # -----------------------------------------------------------------------------------------
    def hud(self):
        F = self.F
        grey = '#8A8A8A'

        def glyph(score, k_for_zero_hex=None):
            out = []
            out.append(f'execute if score {score} mb matches 0 run data modify storage rlk:mboss %s append value {{text:"◇",color:"{grey}"}}')
            for e in range(1, 5):
                out.append(f'execute if score {score} mb matches {e} run data modify storage rlk:mboss %s append value '
                           f'{{text:"◆",color:"{A.EL_HEX[e]}"}}')
            return out

        extra = ['# Name-line suffix (D21): the two record slots of this cycle (◇ empty, ◆ element colour) + the state.',
                 'data modify storage rlk:mboss extra set value [{text:"   기록 ",color:"#B0A890",bold:false}]']
        extra += [l % 'extra' for l in glyph('#gdSlotA')]
        extra += [l % 'extra' for l in glyph('#gdSlotB')]
        extra += [f'execute if score #gdSt mb matches {ST["guard"]} run data modify storage rlk:mboss extra append value {{text:"  · 파수 모드",color:"#FCE484",bold:false}}',
                  f'execute if score #gdSt mb matches {ST["chaos"]} run data modify storage rlk:mboss extra append value {{text:"  · 혼돈",color:"#E03A3A",bold:false}}',
                  f'execute if score #gdSt mb matches {ST["groggy"]} run data modify storage rlk:mboss extra append value {{text:"  · 그로기",color:"#9FE8A0",bold:false}}']
        self.w('hud/extra', extra)
        self.w('hud/sub_intro', [F('hud/extra'),
                                 'data modify storage rlk:mboss sub set value [{text:"개안자 · 세계 망루의 파수꾼",color:"#C8C0A8"}]'])
        self.w('hud/sub_idle', [F('hud/extra'), f'data modify storage rlk:mboss sub set value [{{text:"대기",color:"{grey}"}}]'])
        pat = [F('hud/extra')]
        for p in self.pats:
            if p.kind == 'normal':
                pat.append(f'execute if score #gdPick mb matches {p.id} run data modify storage rlk:mboss sub set value '
                           f'[{{text:"패턴  ",color:"#A8A8A8"}},{{text:"{p.label}",color:"#FFD86B"}}]')
        self.w('hud/sub_pattern', pat)
        gsub = [F('hud/extra'),
                'data modify storage rlk:mboss sub set value [{text:"파수 모드 ",color:"#FCE484",bold:true}]',
                'execute if score #gdGN mb matches 1 run data modify storage rlk:mboss sub append value {text:"I   ",color:"#FCE484",bold:true}',
                'execute if score #gdGN mb matches 2 run data modify storage rlk:mboss sub append value {text:"II   ",color:"#FCE484",bold:true}',
                'execute if score #gdGP mb matches 3.. run data modify storage rlk:mboss sub append value {text:"휘두르기!",color:"#FFB070",bold:true}',
                'execute if score #gdGP mb matches 3.. run return 0',
                'data modify storage rlk:mboss sub append value {text:"원소 기록  ",color:"#B0A890"}']
        for e in range(1, 5):
            h = A.EL_HEX[e]
            gsub.append(f'data modify storage rlk:mboss sub append value {{text:"{A.EL_KO[e]} ",color:"{h}",extra:['
                        f'{{score:{{name:"#gdN{e}",objective:"mb"}}}},{{text:"/"}},'
                        f'{{score:{{name:"#gdQ{e}",objective:"mb"}}}},{{text:"   "}}]}}')
        self.w('hud/sub_guard', gsub)
        self.w('hud/sub_chaos_in', [F('hud/extra'),
                                    'data modify storage rlk:mboss sub set value [{text:"혼돈  ",color:"#E03A3A",bold:true},{text:"신성한 붉은 에너지",color:"#E8B8B8"}]'])
        csub = [F('hud/extra'),
                'data modify storage rlk:mboss sub set value [{text:"혼돈  ",color:"#E03A3A",bold:true},{text:"원소별 ",color:"#E8B8B8"}]']
        for slot in (1, 2):
            csub.append(f'execute if score #gdSa{slot} mb matches 0 run data modify storage rlk:mboss sub append value {{text:"◇ ",color:"{grey}"}}')
            for k in range(1, 7):
                csub.append(f'execute if score #gdSa{slot} mb matches 1 if score #gdSk{slot} mb matches {k} run data modify storage rlk:mboss sub append value '
                            f'{{text:"✦ ",color:"{A.STAR_HEX[k]}"}}')
        csub.append('data modify storage rlk:mboss sub append value {text:"  남은 시간 ",color:"#E8B8B8",extra:['
                    '{score:{name:"#gdTimS",objective:"mb"},color:"#FFFFFF"},{text:"초"}]}')
        self.w('hud/sub_chaos', csub)
        self.w('hud/sub_fail', [F('hud/extra'),
                                'data modify storage rlk:mboss sub set value [{text:"파괴 실패  ",color:"#E06A5A",bold:true},{text:"거대한 창이 떨어진다",color:"#E8B8B8"}]'])
        self.w('hud/sub_groggy', [F('hud/extra'),
                                  'data modify storage rlk:mboss sub set value [{text:"그로기  ",color:"#9FE8A0",bold:true},{text:"공격할 기회",color:"#C8E8C8"}]'])
        bg = ['# @s = body: the leading element\'s record progress (count x 100 / needed) in its colour; gold time left',
              '# before the first counted hit.',
              sc_set('#gdBest', -1), sc_set('#gdBestE', 0)]
        for e in range(1, 5):
            bg += [f'scoreboard players operation #gdX mb = #gdN{e} mb', 'scoreboard players operation #gdX mb *= #c100 mb',
                   f'scoreboard players operation #gdX mb /= #gdQ{e} mb',
                   f'execute if score #gdN{e} mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players set #gdBestE mb {e}',
                   f'execute if score #gdN{e} mb matches 1.. if score #gdX mb > #gdBest mb run scoreboard players operation #gdBest mb = #gdX mb']
        bg += [f'execute if score #gdBestE mb matches 0 run scoreboard players set #buSub bu {GUARD_END}',
               'execute if score #gdBestE mb matches 0 run scoreboard players operation #buSub bu -= #gdT mb',
               f'execute if score #gdBestE mb matches 0 run scoreboard players set #buSubMax bu {GUARD_ACTIVE}',
               'execute if score #gdBestE mb matches 0 run scoreboard players set #buSubCol bu 8',
               'execute if score #gdBestE mb matches 0 run return 0',
               'scoreboard players operation #buSub bu = #gdBest mb', 'scoreboard players set #buSubMax bu 100']
        bg += [f'execute if score #gdBestE mb matches {e} run scoreboard players set #buSubCol bu {A.EL_BU[e]}' for e in range(1, 5)]
        self.w('hud/bar_guard', bg)
        self.w('hud/bar_chaos', ['scoreboard players operation #buSub bu = #gdTim mb', sc_set_bu('#buSubMax', CHAOS_TIMER),
                                 sc_set_bu('#buSubCol', 2)])
        self.w('hud/bar_groggy', [sc_set_bu('#buSub', GROGGY), 'scoreboard players operation #buSub bu -= #gdT mb',
                                  sc_set_bu('#buSubMax', GROGGY), sc_set_bu('#buSubCol', 9)])
        self.w('hud/bar_pattern', ['scoreboard players operation #buSub bu = #gdPMax mb', 'scoreboard players operation #buSub bu -= #gdPT mb',
                                   'scoreboard players operation #buSubMax bu = #gdPMax mb', sc_set_bu('#buSubCol', 8)])

    # -----------------------------------------------------------------------------------------
    def tests(self):
        F, R, g = self.F, self.R, self.g
        normal_ids = ', '.join(f'{p.id} {p.label}' for p in self.normal)
        svc = ', '.join(f'{p.id} {p.label}' for p in self.pats if p.kind == 'service')
        HELP = [
            ('1-5', f'다음 패턴 ({normal_ids})'),
            ('11-13', f'바로 실행 ({svc})'),
            ('20 / 21', '파수 모드 I / II(슬롯 A = 번개 기억, 다시 기록 9회)'),
            ('30-33', '혼돈 시작: 지금 슬롯 / 번개+번개 / 타성 둘 / 불+얼음'),
            ('40', '그로기'), ('41', '별 하나 부수기'), ('42', '혼돈 시간 1초 남기기'),
            ('91-94', '원소 타격 기록 흉내(불 물 번개 얼음, 8틱 제한 그대로)'),
            ('99', '대기로'), ('lock 1-5 / 6', '그 패턴만 / 파수 모드 둘 + 혼돈만 반복'),
        ]
        txt = '[{text:"[파수꾼 테스트] ",color:"#E0B84A",bold:true}' + ''.join(
            f',{{text:"{k}",color:"yellow"}},{{text:" {v}  ",color:"gray"}}' for k, v in HELP) + ']'
        self.w('test/help', ['tellraw @a[tag=player] ' + txt])
        self.w('test/cut', [
            '# @s = body: stop whatever runs (hazards, props, pull, movement, slot pattern, guard, chaos).',
            'function rlk:mboss/lib_clear',
            F('p/cancel'),
            F('chaos/reset'),
            sc_set('#gdRecOn', 0), sc_set('#gdRecNew', 0), sc_set('#gdBq1', 0), sc_set('#gdBq2', 0),
            R('spear/geo'), R('eye/geo'),
            g.play('idle'),
            sc_set('#gdCool', 10),
            F('ai/enter')])
        run = ['# @s = body, #gdTst = the requested test id.']
        run += [f'execute if score #gdTst mb matches 1..5 run {F("test/cut")}',
                'execute if score #gdTst mb matches 1..5 run scoreboard players operation #gdReq mb = #gdTst mb',
                'execute if score #gdTst mb matches 1..5 run scoreboard players set #gdCool mb 1',
                'execute if score #gdTst mb matches 1..5 run return 0']
        run += [f'execute if score #gdTst mb matches 11..13 run {F("test/cut")}',
                f'execute if score #gdTst mb matches 12 run {sc_set("#gdSwEl", 3)}',
                f'execute if score #gdTst mb matches 12 run {R("spear/electro")}',
                f'execute if score #gdTst mb matches 13 run {sc_set("#gdFailN", 2)}',
                f'execute if score #gdTst mb matches 13 run {sc_set("#gdFailK1", 5)}',
                f'execute if score #gdTst mb matches 13 run {sc_set("#gdFailK2", 6)}',
                f'execute if score #gdTst mb matches 11..13 run {sc_set("#gdSt", ST["pattern"])}',
                'execute if score #gdTst mb matches 11..13 run scoreboard players operation #gdPat mb = #gdTst mb',
                f'execute if score #gdTst mb matches 11..13 run return run {sc_set("#gdPNew", 1)}']
        run += [f'execute if score #gdTst mb matches 20..21 run {F("test/cut")}',
                f'execute if score #gdTst mb matches 20 run {sc_set("#gdSlotA", 0)}',
                f'execute if score #gdTst mb matches 21 run {sc_set("#gdSlotA", 3)}',
                f'execute if score #gdTst mb matches 20 run return run {F("guard/begin1")}',
                f'execute if score #gdTst mb matches 21 run return run {F("guard/begin2")}']
        run += [f'execute if score #gdTst mb matches 30..33 run {F("test/chaos")}',
                'execute if score #gdTst mb matches 30..33 run return 0',
                f'execute if score #gdTst mb matches 40 run {F("test/cut")}',
                f'execute if score #gdTst mb matches 40 run {g.play("chaos_fall")}',
                f'execute if score #gdTst mb matches 40 run return run {F("groggy/begin")}',
                f'execute if score #gdTst mb matches 41 run return run {F("test/break")}',
                'execute if score #gdTst mb matches 42 if score #gdTim mb matches 21.. run scoreboard players set #gdTim mb 20',
                'execute if score #gdTst mb matches 42 run return 0']
        run += [f'execute if score #gdTst mb matches {90 + e} run scoreboard players set #elem tmp {e}' for e in range(1, 5)]
        run += ['execute if score #gdTst mb matches 91..94 run scoreboard players set #tfm tmp 0',
                f'execute if score #gdTst mb matches 91..94 run return run {F("on_hit")}',
                f'execute if score #gdTst mb matches 99 run return run {F("test/cut")}',
                F('test/help')]
        self.w('test/run', run)
        self.w('test/chaos', [
            f'# Chaos now with preset slots (30 = keep, 31 = electro x2, 32 = inert x2, 33 = pyro + cryo).',
            'scoreboard players operation #gdX mb = #gdSlotA mb', 'scoreboard players operation #gdY mb = #gdSlotB mb',
            F('test/cut'),
            'scoreboard players operation #gdSlotA mb = #gdX mb', 'scoreboard players operation #gdSlotB mb = #gdY mb',
            f'execute if score #gdTst mb matches 31 run {sc_set("#gdSlotA", 3)}',
            f'execute if score #gdTst mb matches 31 run {sc_set("#gdSlotB", 3)}',
            f'execute if score #gdTst mb matches 32 run {sc_set("#gdSlotA", 0)}',
            f'execute if score #gdTst mb matches 32 run {sc_set("#gdSlotB", 0)}',
            f'execute if score #gdTst mb matches 33 run {sc_set("#gdSlotA", 1)}',
            f'execute if score #gdTst mb matches 33 run {sc_set("#gdSlotB", 4)}',
            F('chaos/begin')])
        self.w('test/break', [
            '# Break one living star (as if its pool ran out).',
            'execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star,tag=!rlk_mb_broken,limit=1] run scoreboard players set @s mhpC 0',
            'execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star,tag=!rlk_mb_broken,limit=1] run tag @s add rlk_mb_broken'])


def sc_set_if(cond, v, name, val):
    return f'execute if score {cond} mb matches {v} run scoreboard players set {name} mb {int(val)}'


def sc_set_bu(name, v):
    return f'scoreboard players set {name} bu {int(v)}'
