"""Balance gauge (균형치) and groggy (그로기) for every enemy — the shared layer rlk:bal/** (combat overhaul lane B).

    python3 tools/build_balance.py [--resourcepack <unpacked resource pack>]

Writes data/rlk/function/bal/** (stale files there are removed, so any number of runs gives the same tree) and, with
--resourcepack, the font rlk:bal (assets/rlk/font/bal.json + assets/rlk/textures/font/bal/*.png, PUA band U+ED00).

Interface (plan.md, lane B owns rlk:bal/**; scores on the enemy's damage-taking entity: the cm brain, the vanilla mob,
the mid / chapter / special boss body rlk_mb_body, Raiden rlk_raiden):
  bal      pips left (0..balMax)            balMax  pips of a full gauge (0 = no gauge: never reduced, never groggy)
  balT     regen countdown (ticks to the next +1 pip while pips are missing; 1 while groggy or pending; 0 = idle)
  grgT     groggy ticks left (groggy = grgT matches 1..)
  execute as <enemy> run function rlk:bal/hit {n:<pips>}
           takes n pips (returns 1 if it took them, fails if the enemy has no gauge, is groggy, depleted-and-pending or
           in a state that refuses balance damage); at 0 the groggy starts (bosses: as soon as their module allows it).
  execute as <boss> run function rlk:bal/refill
           a boss module's own mechanic groggy (break / stun / down) refills the gauge and drops a pending balance groggy.
Internal: balC tier (1 normal, 2 elite, 3 boss), balF flash ticks of the pip just lost, balQ / balX game time of the last
burst / reaction balance loss (per-target windows); tags rlk_bal_grog (groggy), rlk_bal_noai (NoAI before the groggy),
rlk_bal_pend (boss depleted, waiting for its module's bal_ok); storage rlk:bal (row tables, the boss row `brow`).

Numbers (tunables written by bal/load; README "조절 지점"):
  tier     pips  groggy  damage taken  regen delay  regen step
  normal   4     60 t    +50 %         200 t        60 t / pip
  elite    7     80 t    +40 %         240 t        80 t / pip
  boss     12    100 t   +30 %         300 t        100 t / pip
  regen:   only after `delay` ticks without a balance loss, then +1 pip per `step` until full (Stellar Blade style);
           none while groggy / pending; groggy end = full gauge.
  sources: perfect parry 1 (lane C calls bal/hit {n:1} as the attacker); a burst hit 2 (once per target per 40 t, so a
           multi-hit burst counts once); strong reactions (once per target per 30 t): vaporize 1, melt 1, overload 1,
           superconduct 1, frozen 1, shatter 2, void burn (소각) 1, void judgement (단죄) 1. Burst + reaction on one hit add up.
Families (bal/grog/start): bosses -> their module (mboss/d/bal_on, boss/raiden/bal_on), cm brains -> bal/fam/cm_on
(cancel like a freeze, NoAI, hold; cm/tick keeps them held, rig ticks hold the pose), other mobs -> bal/fam/va_on (NoAI).
"""
import argparse
import json
import shutil
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/rlk/function/bal'
ap = argparse.ArgumentParser()
ap.add_argument('--resourcepack')
RP = Path(ap.parse_args().resourcepack) if ap.parse_args().resourcepack else None

# ---------------------------------------------------------------- numbers
TIERS = {1: dict(name='normal', pips=4, grg=60, amp=150, rd=200, rs=60),
         2: dict(name='elite', pips=7, grg=80, amp=140, rd=240, rs=80),
         3: dict(name='boss', pips=12, grg=100, amp=130, rd=300, rs=100)}
BURST_PIPS, BURST_GAP = 2, 40
RX_GAP = 30
# reaction id (#rx tmp, element/react) -> pips
RX_PIPS = {1: 1, 2: 1, 3: 1, 4: 1, 6: 1, 7: 2, 17: 1, 19: 1}
FLASH = 6                       # ticks the pip just lost shows white
# ---------------------------------------------------------------- glyphs (font rlk:bal, PUA U+ED00..)
FONT = 'rlk:bal'
G = {'hf': 0xED00, 'he': 0xED01, 'hx': 0xED02, 'hg': 0xED03,      # head row: 7x7 filled / empty / flash / groggy
     'bf': 0xED10, 'be': 0xED11, 'bx': 0xED12, 'bg': 0xED13,      # boss row: 5x5, rows 14-18 of the bossui line
     'sp': 0xED20, 'bpad': 0xED21, 'bneg': 0xED22}
C = {k: chr(v) for k, v in G.items()}
HEAD_PX, BOSS_PX = 7, 5
GAP = 2                         # the space after each pip: pitch = glyph + bitmap advance 1 + GAP (video: 7 px at 10.5 px)
HEAD_PITCH = HEAD_PX + 1 + GAP
BOSS_PITCH = BOSS_PX + 1 + GAP
BAR = 200                       # bossui bar width (tools/build_bossbar.py BAR)
BOSS_W = TIERS[3]['pips'] * BOSS_PITCH
BOSS_PAD = BAR - BOSS_W         # the boss row: back BAR px (bneg), the pips, the pad -> it adds no width to the bossui line
HEAD_SCALE = 0.5                # text_display scale; 1 font px = 0.025 b at scale 1
HEAD_Y = 0.02                   # under the shield / erosion band (0.15..0.25) and the HP bar (0.25..0.38)
YELLOW, GREY, WHITE, GROG = (0xFF, 0xD2, 0x3F), (0x5E, 0x5E, 0x5E), (0xFF, 0xFF, 0xFF), (0xFF, 0x6A, 0x3C)


def head_x(pips):
    """Translation x that puts the row's left end at the HP bar's left end (-0.8)."""
    w = pips * HEAD_PITCH * 0.025 * HEAD_SCALE
    return round(-0.8 + w / 2, 4)


# ---------------------------------------------------------------- datapack
files = {}


def f(name, *lines):
    files[name] = '\n'.join(lines) + '\n'


def tier_set(dst, key, src='@s'):
    """dst = the tier's value of key (constant scores #<key><tier> bal)."""
    return [f'execute if score {src} balC matches {t} run scoreboard players operation {dst} = #{key}{t} bal' for t in TIERS]


def row(n, maxp, flash, groggy, kind):
    """A row component: n filled, then (flash) one white pip, then empty pips (kind 'h' head / 'b' boss)."""
    if groggy:
        s = (C[kind + 'g'] + C['sp']) * maxp
    else:
        s = (C[kind + 'f'] + C['sp']) * n
        k = n
        if flash and n < maxp:
            s += C[kind + 'x'] + C['sp']
            k += 1
        s += (C[kind + 'e'] + C['sp']) * (maxp - k)
    if kind == 'b':
        s = C['bneg'] + s + C['bpad']
    return {'text': '', 'extra': [{'text': s, 'font': FONT, 'color': 'white'}]}


def table(maxp, kind):
    """Index: 0..max = plain (n filled), max+1+n = n filled + flash (n < max), 2*max+1 = groggy."""
    t = [row(n, maxp, False, False, kind) for n in range(maxp + 1)]
    t += [row(n, maxp, True, False, kind) for n in range(maxp)]
    t.append(row(0, maxp, False, True, kind))
    return t


def snbt(v):
    if isinstance(v, dict):
        return '{' + ','.join(f'{k}:{snbt(x)}' for k, x in v.items()) + '}'
    if isinstance(v, list):
        return '[' + ','.join(snbt(x) for x in v) + ']'
    return json.dumps(v, ensure_ascii=False)


load = ['# @s = server (from rlk:load). Objectives, tunables (README "조절 지점") and the row tables of the balance gauge.',
        '# Generated by tools/build_balance.py: edit the generator, not this file.']
for o in ('bal', 'balMax', 'balT', 'grgT', 'balC', 'balF', 'balQ', 'balX'):
    load.append(f'scoreboard objectives add {o} dummy')
for t, d in TIERS.items():
    load.append(f'# {d["name"]}: {d["pips"]} pips, groggy {d["grg"]} t (damage taken {d["amp"]} %), '
                f'regen after {d["rd"]} t then +1 pip per {d["rs"]} t')
    for k in ('pips', 'grg', 'amp', 'rd', 'rs'):
        load.append(f'scoreboard players set #{k}{t} bal {d[k]}')
load += [f'# sources: a burst hit takes {BURST_PIPS} pips, once per target per {BURST_GAP} t; strong reactions once per target per {RX_GAP} t',
         f'scoreboard players set #burst bal {BURST_PIPS}',
         f'scoreboard players set #burstGap bal {BURST_GAP}',
         f'scoreboard players set #rxGap bal {RX_GAP}',
         f'scoreboard players set #flash bal {FLASH}',
         'scoreboard players set #100 bal 100']
for m in sorted({TIERS[1]['pips'], TIERS[2]['pips']}):
    load.append(f'data modify storage rlk:bal h{m} set value {snbt(table(m, "h"))}')
load.append(f'data modify storage rlk:bal b{TIERS[3]["pips"]} set value {snbt(table(TIERS[3]["pips"], "b"))}')
load += ['# mobs that existed before this layer (a /reload into an older world) get their gauge now',
         'execute as @e[tag=rlk_mob] unless score @s balMax matches 0.. at @s run function rlk:bal/init']
f('load', *load)

f('init',
  '# @s = a new enemy, at @s (mob/setup, after rlk_mob): its tier, a full gauge and (normal / elite) the pip row under the',
  '# head bar. Excluded (no gauge, never groggy): mechanic objects and stand-ins (boss aux / hit objects and proxies,',
  '# Raiden objects, spore pods, cicin summons, lobby dummies); pets never reach mob/setup.',
  '# A mob set up again (a burrower surfacing) keeps its gauge and gets its row back.',
  'execute if score @s balMax matches 0.. run return run function rlk:bal/re_init',
  'scoreboard players set @s balMax 0',
  'scoreboard players set @s balC 0',
  'scoreboard players set @s bal 0',
  'scoreboard players set @s balT 0',
  'scoreboard players set @s grgT 0',
  'execute if entity @s[tag=rlk_mb_aux] run return 0',
  'execute if entity @s[tag=rlk_mb_hit] run return 0',
  'execute if entity @s[tag=rlk_mb_px] run return 0',
  'execute if entity @s[tag=rlk_rd_object] run return 0',
  'execute if entity @s[tag=rlk_c3pod] run return 0',
  'execute if entity @s[tag=rlk_cm_ci] run return 0',
  'execute if entity @s[tag=rlk_lobby] run return 0',
  'execute if entity @s[tag=rlk_pet] run return 0',
  '# bosses: a registry boss only when its module implements the balance hooks (registry "bal", mboss/d/bal_has)',
  'execute if entity @s[tag=rlk_mb_body] unless function rlk:mboss/d/bal_has run return run data remove storage rlk:bal brow',
  'execute if entity @s[tag=rlk_mb_body] run scoreboard players set @s balC 3',
  'execute if entity @s[tag=rlk_raiden] run scoreboard players set @s balC 3',
  'execute if score @s balC matches 0 if entity @s[tag=rlk_c2e] run scoreboard players set @s balC 2',
  'execute if score @s balC matches 0 if entity @s[tag=rlk_c3e] run scoreboard players set @s balC 2',
  'execute if score @s balC matches 0 run scoreboard players set @s balC 1',
  *tier_set('@s balMax', 'pips'),
  'scoreboard players operation @s bal = @s balMax',
  'scoreboard players set @s balF 0',
  'scoreboard players set @s balQ 0',
  'scoreboard players set @s balX 0',
  'execute if score @s balC matches 1..2 run function rlk:bal/ui/row_new',
  'function rlk:bal/ui/draw')
f('re_init',
  '# @s = an enemy set up again (mob/setup): the gauge stays; a normal / elite whose row went with its old head bar gets one',
  'execute unless score @s balC matches 1..2 run return 0',
  'scoreboard players set #has bal 0',
  'execute on passengers if entity @s[tag=rlk_hb_bal] run scoreboard players set #has bal 1',
  'execute if score #has bal matches 0 run function rlk:bal/ui/row_new',
  'function rlk:bal/ui/draw')

f('hit',
  '# API (lane C: perfect parry): execute as <enemy> run function rlk:bal/hit {n:<pips>}',
  '$scoreboard players set #n bal $(n)',
  'return run function rlk:bal/take')
f('take',
  '# @s = enemy, #n bal = pips to take. Returns 1 when taken; fails without a gauge, while groggy / pending, or when the',
  '# enemy refuses balance damage now (bosses: intro, death, cutscene, hidden bars; Raiden: see bal/boss/may).',
  'execute unless score @s balMax matches 1.. run return fail',
  'execute if score @s grgT matches 1.. run return fail',
  'execute if entity @s[tag=rlk_bal_pend] run return fail',
  'execute unless score #n bal matches 1.. run return fail',
  'execute if score @s balC matches 3 unless function rlk:bal/boss/may run return fail',
  'scoreboard players operation @s bal -= #n bal',
  'execute if score @s bal matches ..-1 run scoreboard players set @s bal 0',
  *tier_set('@s balT', 'rd'),
  'scoreboard players operation @s balF = #flash bal',
  'execute if score @s bal matches 0 run function rlk:bal/grog/try',
  'execute unless score @s grgT matches 1.. run function rlk:bal/ui/draw',
  'return 1')

f('refill',
  '# API for the boss modules: @s = boss whose own mechanic groggy (a break, a stun, a down) starts — the balance gauge',
  '# is full again and a pending balance groggy is dropped, so the two never chain. Nothing while a balance groggy runs.',
  'execute unless score @s balMax matches 1.. run return 0',
  'execute if score @s grgT matches 1.. run return 0',
  'tag @s remove rlk_bal_pend',
  'scoreboard players operation @s bal = @s balMax',
  'scoreboard players set @s balT 0',
  'scoreboard players set @s balF 0',
  'function rlk:bal/ui/draw')

# ---------------------------------------------------------------- the damage path (combat/apply_mods, one line)
f('mods',
  '# @s = enemy with a gauge, in combat/apply_mods (after element/on_hit, before the boss incoming hooks / HP floors; never',
  '# true damage): a groggy enemy takes the tier %, else a burst hit / a strong reaction takes balance (not on a killing blow)',
  'execute if score @s grgT matches 1.. run return run function rlk:bal/amp',
  'execute unless score #burstDmg tmp matches 1.. unless score #rx tmp matches 1.. run return 0',
  'execute if score #dmg tmp >= @s mhpC run return 0',
  'function rlk:bal/src/hit')
f('src/hit',
  '# @s = enemy with pips left (bal/mods). A burst hit (#burstDmg tmp = the game time of the burst\'s damage calc, set by',
  '# items/hook/burst_dmg, cleared by char/after_hit) and a strong reaction (#rx tmp, element/react) take balance; their',
  '# per-target windows make a multi-hit burst or a chain of reactions count once.',
  'scoreboard players set #n bal 0',
  'execute store result score #now bal run time query gametime',
  'execute if score #burstDmg tmp = #now bal run function rlk:bal/src/burst',
  'execute if score #rx tmp matches 1.. run function rlk:bal/src/rx',
  'execute if score #n bal matches 1.. run function rlk:bal/take')
f('src/burst',
  'scoreboard players operation #d bal = #now bal',
  'scoreboard players operation #d bal -= @s balQ',
  'execute if score #d bal < #burstGap bal run return 0',
  'scoreboard players operation @s balQ = #now bal',
  'scoreboard players operation #n bal += #burst bal')
rx = ['# strong reactions (#rx: 1 vaporize 2 melt 3 overload 4 superconduct 6 frozen 7 shatter 17 void burn 19 void judgement)',
      'scoreboard players set #r bal 0']
for k, v in sorted(RX_PIPS.items()):
    rx.append(f'execute if score #rx tmp matches {k} run scoreboard players set #r bal {v}')
rx += ['execute if score #r bal matches 0 run return 0',
       'scoreboard players operation #d bal = #now bal',
       'scoreboard players operation #d bal -= @s balX',
       'execute if score #d bal < #rxGap bal run return 0',
       'scoreboard players operation @s balX = #now bal',
       'scoreboard players operation #n bal += #r bal']
f('src/rx', *rx)
f('amp',
  '# @s = groggy enemy (combat/apply_mods, before the boss incoming hooks and their HP floors): #dmg x the tier %',
  *tier_set('#a bal', 'amp'),
  'scoreboard players operation #dmg tmp *= #a bal',
  'scoreboard players operation #dmg tmp /= #100 bal')

# ---------------------------------------------------------------- per tick
f('tick',
  '# @s = enemy, at @s (mob/tick while balT >= 1; Raiden runs bal/boss/tick from her own tick): groggy countdown, else the',
  '# flash and the regen. A registry boss only while its fight runs (#mbSt 1, not paused: the clocks stop with the fight).',
  'execute if score @s balC matches 3 run return run function rlk:bal/boss/tick_mob',
  'execute if score @s grgT matches 1.. run return run function rlk:bal/grog/tick',
  'function rlk:bal/regen_tick')
f('boss/tick_mob',
  'execute unless score #mbSt mb matches 1 run return 0',
  'execute if score #mbPause mb matches 1 run return 0',
  'function rlk:bal/boss/tick')
f('regen_tick',
  '# @s = enemy with pips missing: the white pip goes back to empty, and after the delay +1 pip per step',
  'execute if score @s balF matches 1.. run function rlk:bal/flash',
  'scoreboard players remove @s balT 1',
  'execute if score @s balT matches ..0 run function rlk:bal/regen')
f('flash',
  'scoreboard players remove @s balF 1',
  'execute if score @s balF matches ..0 run function rlk:bal/ui/draw')
f('regen',
  'scoreboard players add @s bal 1',
  'execute if score @s bal >= @s balMax run scoreboard players operation @s bal = @s balMax',
  *tier_set('@s balT', 'rs'),
  'execute if score @s bal = @s balMax run scoreboard players set @s balT 0',
  'scoreboard players set @s balF 0',
  'function rlk:bal/ui/draw')

# ---------------------------------------------------------------- groggy
f('grog/try',
  '# @s = enemy whose gauge just hit 0: groggy now, or (a boss in a state its module protects) as soon as it allows',
  'execute if score @s balC matches 3 unless function rlk:bal/boss/ok run return run function rlk:bal/boss/pend_on',
  'function rlk:bal/grog/start')
f('grog/start',
  '# @s = enemy, at @s: the groggy starts (tier length); the family stops the enemy cleanly',
  *tier_set('@s grgT', 'grg'),
  'scoreboard players set @s balT 1',
  'scoreboard players set @s balF 0',
  'scoreboard players set @s bal 0',
  'tag @s add rlk_bal_grog',
  'tag @s remove rlk_bal_pend',
  'function rlk:bal/fx/start',
  'execute if score @s balC matches 3 if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/bal_on',
  'execute if score @s balC matches 3 if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/bal_on',
  'execute if score @s balC matches 1..2 if entity @s[tag=rlk_cmb] run function rlk:bal/fam/cm_on',
  'execute if score @s balC matches 1..2 unless entity @s[tag=rlk_cmb] run function rlk:bal/fam/va_on',
  'function rlk:bal/ui/draw')
f('grog/tick',
  '# @s = groggy normal / elite enemy, at @s (bal/tick)',
  'scoreboard players remove @s grgT 1',
  'execute if score @s grgT matches ..0 run return run function rlk:bal/grog/end',
  'scoreboard players operation #m bal = @s grgT',
  'scoreboard players set #k bal 16',
  'scoreboard players operation #m bal %= #k bal',
  'scoreboard players operation #e bal = #m bal',
  'scoreboard players set #k bal 2',
  'scoreboard players operation #e bal %= #k bal',
  'execute if score #e bal matches 0 on passengers if entity @s[tag=rlk_hb_bal] at @s run function rlk:bal/fx/dizzy')
f('grog/end',
  '# @s = enemy, at @s: the groggy ends, the gauge is full again and the family resumes the enemy',
  'scoreboard players set @s grgT 0',
  'tag @s remove rlk_bal_grog',
  'scoreboard players operation @s bal = @s balMax',
  'scoreboard players set @s balT 0',
  'scoreboard players set @s balF 0',
  'execute if score @s balC matches 3 if entity @s[tag=rlk_mb_body] run function rlk:mboss/d/bal_off',
  'execute if score @s balC matches 3 if entity @s[tag=rlk_raiden] run function rlk:boss/raiden/bal_off',
  'execute if score @s balC matches 1..2 if entity @s[tag=rlk_cmb] run function rlk:bal/fam/cm_off',
  'execute if score @s balC matches 1..2 unless entity @s[tag=rlk_cmb] run function rlk:bal/fam/va_off',
  'playsound minecraft:block.beacon.power_select hostile @a ~ ~ ~ 0.5 1.6',
  'function rlk:bal/ui/draw')
f('grog/clear',
  '# @s = groggy enemy (bal/uninstall): undo what the family changed on the entity, no sound, no redraw',
  'scoreboard players set @s grgT 0',
  'tag @s remove rlk_bal_grog',
  'execute if score @s balC matches 1..2 run function rlk:bal/fam/noai_off')

# ---- families
f('fam/noai_on',
  '# NoAI for the groggy, remembering whether the mob had it before (a freeze that is on holds that in rlk_noai)',
  'execute if score @s frzT matches 1.. if entity @s[tag=rlk_noai] run tag @s add rlk_bal_noai',
  'execute unless score @s frzT matches 1.. if data entity @s {NoAI:1b} run tag @s add rlk_bal_noai',
  'data merge entity @s {NoAI:1b}')
f('fam/noai_off',
  '# a freeze still on keeps NoAI and restores the mob\'s own state when it ends (element/frz_end); else restore it here',
  'execute if score @s frzT matches 1.. run return run function rlk:bal/fam/noai_pass',
  'execute unless entity @s[tag=rlk_bal_noai] run data merge entity @s {NoAI:0b}',
  'tag @s remove rlk_bal_noai')
f('fam/noai_pass',
  'tag @s remove rlk_noai',
  'execute if entity @s[tag=rlk_bal_noai] run tag @s add rlk_noai',
  'tag @s remove rlk_bal_noai')
f('fam/va_on',
  '# vanilla-AI mob (husk / skeleton / vindicator, #mobTmp rooms): AI off (slowness does not stop a bow or a bite)',
  'function rlk:bal/fam/noai_on')
f('fam/va_off',
  'function rlk:bal/fam/noai_off')
f('fam/cm_on',
  '# cm brain: the freeze path without the ice — the running attack is cancelled (lines, fireballs, cannon aim, charge',
  '# tag; elites reset on their next tick: dash targets, nj visible, cs surfaced), the drummer stops, AI off, held',
  'scoreboard players operation #cid tmp = @s cmId',
  'function rlk:cm/cancel',
  'execute if entity @s[tag=rlk_cm_dr] run function rlk:cm/dr/interrupt',
  'function rlk:bal/fam/noai_on',
  'scoreboard players set @s stunT 2',
  'function rlk:bal/fam/cm_hold')
f('fam/cm_hold',
  '# keep the cooldowns from running out during the groggy: casters that start while stunned (ar fm im cn) need cmCd 0',
  'execute unless score @s cmCd matches 10.. run scoreboard players set @s cmCd 10',
  'execute unless score @s cmCd2 matches 10.. run scoreboard players set @s cmCd2 10')
f('fam/cm_tick',
  '# @s = groggy cm brain (cm/tick, after the freeze line): not free, held in place, stunned for the group starts',
  '# (pack_go / line_go / pair_go skip stunned members, rv/fly hangs), nothing started',
  'scoreboard players set #free tmp 0',
  'scoreboard players set #hold tmp 1',
  'execute unless score @s stunT matches 2.. run scoreboard players set @s stunT 2',
  'function rlk:bal/fam/cm_hold',
  'execute if score @s cmS matches 1.. run function rlk:cm/cancel')
f('fam/cm_off',
  '# the next mob/tick sees stunT 0 and runs mob/unstun (slowness, team); cmCd >= 10 gives a short breather',
  'function rlk:bal/fam/noai_off',
  'scoreboard players set @s stunT 0')

# ---- bosses
f('boss/tick',
  '# @s = boss body, at @s (mob/tick -> bal/tick -> boss/tick_mob for a registry boss, boss/raiden/tick for Raiden, while',
  '# balT >= 1; a paused fight does not run it)',
  'execute if entity @s[tag=rlk_bal_pend] run return run function rlk:bal/boss/pend_tick',
  'execute if score @s grgT matches 1.. run return run function rlk:bal/boss/grog_tick',
  'function rlk:bal/regen_tick')
f('boss/grog_tick',
  'scoreboard players remove @s grgT 1',
  'execute if score @s grgT matches ..0 run function rlk:bal/grog/end')
f('boss/pend_on',
  '# @s = boss at 0 pips in a state its module protects: groggy at the first tick bal_ok allows it',
  'tag @s add rlk_bal_pend',
  'scoreboard players set @s bal 0',
  'scoreboard players set @s balT 1',
  'scoreboard players set @s balF 0')
f('boss/pend_tick',
  'scoreboard players set @s balT 1',
  'execute if function rlk:bal/boss/may if function rlk:bal/boss/ok run function rlk:bal/grog/start')
f('boss/may',
  '# @s = boss: may it take balance damage now? Registry bosses: only in the fight state, outside cutscenes and hidden',
  '# bars (scarlet cines), and only while the body is in play - not untargetable (rlk_mb_inv: parked for a phase the',
  '# player fights something else in, under the floor, away in the air; review B-09: perfect parries of the creatures\'',
  '# shots emptied the parked Apep\'s gauge); Raiden: the Shogun phase only (Tenma\'s armour is its gauge), not in the',
  '# transformation, the exhausted / stunned / finishing states, a blink or the death',
  'execute if entity @s[tag=rlk_mb_body] unless score #mbSt mb matches 1 run return fail',
  'execute if entity @s[tag=rlk_mb_body] if score #mbCine mb matches 1 run return fail',
  'execute if entity @s[tag=rlk_mb_body] if score #mbBarOff mb matches 1 run return fail',
  'execute if entity @s[tag=rlk_mb_body,tag=rlk_mb_inv] run return fail',
  # hr FN-bal (hr_design §1.3, mboss_scarlet api.BAL_OFF): a module holds #mbBalOff mb 1 while its bars are on but she takes no
  # balance damage (홍련: the lead-ins and the gauntlets); fight_vars / cleanup_fight zero it
  'execute if entity @s[tag=rlk_mb_body] if score #mbBalOff mb matches 1 run return fail',
  'execute if entity @s[tag=rlk_mb_dying] run return fail',
  'execute if entity @s[tag=rlk_raiden] unless score @s rdPhase matches 0 run return fail',
  'execute if entity @s[tag=rlk_raiden] if score @s rdDeath matches 1.. run return fail',
  'execute if entity @s[tag=rlk_raiden] if score @s rdPat matches 98..99 run return fail',
  'return 1')
f('boss/ok',
  '# @s = boss: may the groggy start now? (the module knows its scripted / invulnerable / mechanic states)',
  'execute if entity @s[tag=rlk_mb_body] run return run function rlk:mboss/d/bal_ok',
  'execute if entity @s[tag=rlk_raiden] run return run function rlk:boss/raiden/bal_ok',
  'return fail')

# ---------------------------------------------------------------- look and sound
f('fx/start',
  '# @s = enemy, at @s: the balance breaks — a yellow burst at the head and a shield-break crack',
  'playsound minecraft:item.shield.break hostile @a ~ ~ ~ 1.0 0.7',
  'playsound minecraft:block.anvil.land hostile @a ~ ~ ~ 0.3 1.8',
  'execute if score @s balC matches 1..2 on passengers if entity @s[tag=rlk_hb_bal] at @s run function rlk:bal/fx/burst',
  'execute if score @s balC matches 3 positioned ~ ~2.2 ~ run function rlk:bal/fx/burst')
f('fx/burst',
  'particle minecraft:flash{color:[1.0f,0.82f,0.25f,1.0f]} ~ ~0.3 ~ 0 0 0 0 1',
  'particle minecraft:dust{color:[1.0f,0.82f,0.25f],scale:1.2f} ~ ~0.3 ~ 0.35 0.2 0.35 0 14',
  'particle minecraft:crit ~ ~0.3 ~ 0.3 0.2 0.3 0.25 10')
dizzy = ['# at the head anchor of a groggy enemy (#m bal = grgT mod 16): two yellow stars circling over the head, a step',
         '# every 2 ticks']
import math
for i in range(8):
    a = math.radians(i * 45)
    x, z = round(0.42 * math.cos(a), 2), round(0.42 * math.sin(a), 2)
    dizzy.append(f'execute if score #m bal matches {2 * i}..{2 * i + 1} run particle minecraft:dust{{color:[1.0f,0.86f,0.3f],scale:0.8f}} '
                 f'~{x} ~0.55 ~{z} 0 0 0 0 1')
    dizzy.append(f'execute if score #m bal matches {2 * i}..{2 * i + 1} run particle minecraft:dust{{color:[1.0f,0.86f,0.3f],scale:0.8f}} '
                 f'~{-x} ~0.55 ~{-z} 0 0 0 0 1')
f('fx/dizzy', *dizzy)

# ---------------------------------------------------------------- the rows
f('ui/row_new',
  '# @s = normal / elite enemy, at @s: the pip row (text_display) rides it with the head bar, left end at the bar\'s left end',
  *[f'execute if score @s balMax matches {d["pips"]} run summon minecraft:text_display ~ ~ ~ '
    '{Tags:["rlk_hb_bal","rlk_bal_new"],billboard:"center",alignment:"center",see_through:true,background:0,shadow:false,'
    f'text:"",transformation:{{translation:[{head_x(d["pips"])}f,{HEAD_Y}f,0.06f],scale:[{HEAD_SCALE}f,{HEAD_SCALE}f,{HEAD_SCALE}f],'
    'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}' for t, d in TIERS.items() if t < 3],
  'ride @e[tag=rlk_bal_new,limit=1] mount @s',
  'tag @e[tag=rlk_bal_new] remove rlk_bal_new')
f('ui/draw',
  '# @s = enemy: the row index (0..max plain, max+1+n flash, 2*max+1 groggy) -> head text / the boss row storage',
  'scoreboard players operation #i bal = @s bal',
  'execute if score @s balF matches 1.. if score @s bal < @s balMax run scoreboard players operation #i bal += @s balMax',
  'execute if score @s balF matches 1.. if score @s bal < @s balMax run scoreboard players add #i bal 1',
  'execute if score @s grgT matches 1.. run scoreboard players operation #i bal = @s balMax',
  'execute if score @s grgT matches 1.. run scoreboard players operation #i bal += @s balMax',
  'execute if score @s grgT matches 1.. run scoreboard players add #i bal 1',
  'execute store result storage rlk:bal a.i int 1 run scoreboard players get #i bal',
  'execute store result storage rlk:bal a.m int 1 run scoreboard players get @s balMax',
  'execute if score @s balC matches 3 run return run function rlk:bal/ui/boss with storage rlk:bal a',
  'execute on passengers if entity @s[tag=rlk_hb_bal] run function rlk:bal/ui/head with storage rlk:bal a')
f('ui/head', '$data modify entity @s text set from storage rlk:bal h$(m)[$(i)]')
f('ui/boss',
  '# the boss row: back the bossui bar width, the pips, the pad to the bar end (adds no width); the boss bars show it after',
  '# the bossui line ({nbt:"brow",storage:"rlk:bal"} in mboss/bars, boss/raiden/bars)',
  '$data modify storage rlk:bal brow set from storage rlk:bal b$(m)[$(i)]')

f('uninstall',
  '# from rlk:uninstall: groggy mobs get their AI back, the rows go, the scores and the tables go',
  'execute as @e[tag=rlk_bal_grog] run function rlk:bal/grog/clear',
  'tag @e[tag=rlk_bal_pend] remove rlk_bal_pend',
  'kill @e[tag=rlk_hb_bal]',
  *[f'scoreboard objectives remove {o}' for o in ('bal', 'balMax', 'balT', 'grgT', 'balC', 'balF', 'balQ', 'balX')],
  'data remove storage rlk:bal h4',
  'data remove storage rlk:bal h7',
  'data remove storage rlk:bal b12',
  'data remove storage rlk:bal brow',
  'data remove storage rlk:bal a')

# ---------------------------------------------------------------- write
if OUT.exists():
    shutil.rmtree(OUT)
for name, text in files.items():
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


# ---------------------------------------------------------------- resource pack
def png(pixels, w, h):
    raw = b''.join(b'\x00' + b''.join(bytes(pixels[y][x]) for x in range(w)) for y in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)  # noqa: E731
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def diamond(n, fill, rim, inner=None):
    """n x n diamond; rim = outer ring colour (None = fill); inner = (half size, colour) of a centred square only: the
    spent pip, a dim grey square slot as in the video (the cell keeps its full width through two alpha-1 pixels at the
    ends of the middle row)."""
    c = n // 2
    px = [[(0, 0, 0, 0)] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            d = abs(x - c) + abs(y - c)
            if inner:
                if max(abs(x - c), abs(y - c)) <= inner[0]:
                    px[y][x] = (*inner[1], 255)
            elif d <= c:
                px[y][x] = (*(rim if (rim and d == c) else fill), 255)
    if inner:
        px[c][0] = px[c][n - 1] = (0, 0, 0, 1)
    return px


# solid diamonds (a darker rim turns a 5-7 px diamond into a star at GUI scale)
GLYPHS = {'hf': (diamond(7, YELLOW, None), 7, 7), 'he': (diamond(7, None, None, (1, GREY)), 7, 7),
          'hx': (diamond(7, WHITE, None), 7, 7), 'hg': (diamond(7, GROG, None), 7, 7),
          'bf': (diamond(5, YELLOW, None), 5, -7), 'be': (diamond(5, None, None, (1, GREY)), 5, -7),
          'bx': (diamond(5, WHITE, None), 5, -7), 'bg': (diamond(5, GROG, None), 5, -7)}
if RP:
    tex = RP / 'assets/rlk/textures/font/bal'
    if tex.exists():
        shutil.rmtree(tex)
    tex.mkdir(parents=True)
    providers = []
    for k, (px, n, asc) in GLYPHS.items():
        (tex / f'{k}.png').write_bytes(png(px, n, n))
        providers.append({'type': 'bitmap', 'file': f'rlk:font/bal/{k}.png', 'ascent': asc, 'height': n, 'chars': [C[k]]})
    providers.append({'type': 'space', 'advances': {C['sp']: GAP, C['bpad']: BOSS_PAD, C['bneg']: -BAR}})
    providers.append({'type': 'reference', 'id': 'minecraft:default'})
    font = RP / 'assets/rlk/font/bal.json'
    font.parent.mkdir(parents=True, exist_ok=True)
    font.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f'Balance gauge: {len(files)} functions in {OUT.relative_to(ROOT)}'
      + (f'; font {FONT} ({len(GLYPHS)} glyphs) in {RP}' if RP else ' (no --resourcepack: font not written)'))
