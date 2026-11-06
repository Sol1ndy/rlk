"""Build Narukami's hazard engine v2 (plan rd/plan.md B.0; owner S1-KIT): parametric hit volumes, quiet hits, kept
outline decals, separate strike visuals and travelling hazards. The Python API is raiden_kit.hz(); the visuals (decal,
strike and travelling displays, the FX cues) are written by build_raiden_hazard_vfx.build(), called at the end.

Runtime entry points (all under rlk:boss/raiden/hazard/):
  new {k,a..f,tol,tell,dmg,life,ev,max,grp,dk,dl,kb,sv,sm,go,sp,snd,nd,jp,det,lf,fv}   v2 hazard here, yaw = execution yaw
  tick_at (as the marker, at it, rotated as it; world calls it), expire (as the marker), finish (kills the non-detached hazards),
  clear (kills every hazard and kit display), vfx_world (orphaned visuals, the FX card clock), setup (objectives)
Per-hazard scores (milliblocks unless noted):
  rdShape 20 + rdHK · rdHK kind (raiden_kit.KINDS) · rdWind tell · rdDamage · rdHLife · rdHAge
  rdHHit hits so far · rdHMax max hits (0 = no limit) · rdHEv hit interval for follow/field · rdHTol pad
  rdHA..rdHF shape parameters, per kind:
    disk / field / follow / safe_dome  A r, E (r + tol)^2 (safe_dome: r^2), B follow speed (micro-blocks per tick)
    annulus    A rmin, B r, C sin(half)*1000, D cos(half)*1000, E (r + tol)^2, F (rmin - tol)^2
    rect       A len, B half width, C offset;   to_wall  A len (computed at creation), B half width
    sweep      A r0, B v (micro-blocks per tick), C band, D sin(half)*1000, E cos(half)*1000, F travel ticks
    slab       A d0, B v, C half width, D depth, E height, F travel ticks
    orb        A d0, B v, C r, D r + tol, E height of the card, F travel ticks
  rdHGrp hit-sharing group · rdHDk decal id (raiden_kit.DECALS) · rdHDl decal life · rdHKb knock-back steps
  rdHSv strike id (raiden_kit.STRIKES) or the segment count of a sweep · rdHSnd impact sound (1, 2 = + thunder)
  rdHSm strike motion (raiden_kit.STRIKE_MOTION: 0 expand, 1/2 sweep in from her left / right, 3 chop, 4 thrust, 5 rise)
  rdHSp / rdHGo travelling kinds: the rel (ticks from the launch) of the card summon (< 0) and of the start of their
  interpolation (>= 0), raiden_kit.TRAVEL_GAP ticks apart
  rdFX / rdFZ frozen forward vector · rdHId serial (rdVId of its displays) · mlv boss level
Tags: rlk_rd_hazard + rlk_rd_quiet (no decal) / rlk_rd_nododge / rlk_rd_jump / rlk_rd_detached / rlk_rd_lift.
The hit test runs at the tell tick for static kinds, every tick after the launch for travelling ones, and every rdHEv
ticks from the tell for follow / field. It uses the body's feet (rlk_body), never the spectator camera.
"""
from pathlib import Path
import math
import shutil

from raiden_kit import KINDS, SHAPE_BASE, STRIKE_IDS, arc_strike, hz_args

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/rlk/function/boss/raiden/hazard"
H = "rlk:boss/raiden/hazard/"
if OUT.exists():
    shutil.rmtree(OUT)          # this generator owns boss/raiden/hazard/** (no stale v1 frames)
OUT.mkdir(parents=True, exist_ok=True)
NEW = '@e[tag=rlk_rd_hnew,limit=1]'
OBJECTIVES = ['rdHK', 'rdHA', 'rdHB', 'rdHC', 'rdHD', 'rdHE', 'rdHF', 'rdHTol', 'rdHEv', 'rdHMax', 'rdHGrp', 'rdHDk',
              'rdHDl', 'rdHKb', 'rdHSv', 'rdHSnd', 'rdHOX', 'rdHOY', 'rdHOZ', 'rdHNx', 'rdHSm', 'rdHGo', 'rdHSp']
KIT_VERSION = 5


def write(name, lines):
    path = OUT / (name + ".mcfunction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sset(obj, val, who=NEW):
    return f'scoreboard players set {who} {obj} {val}'


# ------------------------------------------------------------------------------------------------ setup / creation
write('setup', ['# Kit objectives (called by vfx/init at load and by the first hazard after a datapack update).'] +
      [f'scoreboard objectives add {o} dummy' for o in OBJECTIVES] +
      ['scoreboard players set #rdOne rd 1', 'scoreboard players set #rdK1000 rd 1000',
       f'scoreboard players set #rdKitV rd {KIT_VERSION}'])

MACRO_KEYS = [('rdHK', 'k'), ('rdHA', 'a'), ('rdHB', 'b'), ('rdHC', 'c'), ('rdHD', 'd'), ('rdHE', 'e'), ('rdHF', 'f'),
              ('rdHTol', 'tol'), ('rdWind', 'tell'), ('rdDamage', 'dmg'), ('rdHLife', 'life'), ('rdHEv', 'ev'),
              ('rdHMax', 'max'), ('rdHGrp', 'grp'), ('rdHDk', 'dk'), ('rdHDl', 'dl'), ('rdHKb', 'kb'), ('rdHSv', 'sv'),
              ('rdHSnd', 'snd'), ('rdHSm', 'sm'), ('rdHGo', 'go'), ('rdHSp', 'sp')]
write('new', [
    '# v2 hazard (raiden_kit.hz). Position = here, yaw = the execution yaw, pitch flattened.',
    'execute unless score #rdKitV rd matches %d run function %ssetup' % (KIT_VERSION, H),
    'summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_hazard","rlk_raiden_aux","rlk_room","rlk_rd_hnew"]}',
    f'tp {NEW} ~ ~ ~ ~ 0',
] + [f'${sset(o, "$(" + k + ")")}' for o, k in MACRO_KEYS] + [
    f'scoreboard players operation {NEW} rdShape = {NEW} rdHK',
    f'scoreboard players add {NEW} rdShape {SHAPE_BASE}',
    '$scoreboard players set #rdFlag rd $(nd)',
    f'execute if score #rdFlag rd matches 1 run tag {NEW} add rlk_rd_nododge',
    '$scoreboard players set #rdFlag rd $(jp)',
    f'execute if score #rdFlag rd matches 1 run tag {NEW} add rlk_rd_jump',
    '$scoreboard players set #rdFlag rd $(det)',
    f'execute if score #rdFlag rd matches 1 run tag {NEW} add rlk_rd_detached',
    '$scoreboard players set #rdFlag rd $(lf)',
    f'execute if score #rdFlag rd matches 1 run tag {NEW} add rlk_rd_lift',
    f'$data modify entity {NEW} data.fv set value $(fv)',
    f'function {H}born',
])
write('born', [
    '# Common creation tail (as the creator): age -1 so the world tick that follows makes it 0 this tick.',
    f'tag {NEW} add rlk_rd_hazard',
    f'scoreboard players set {NEW} rdHAge -1',
    f'scoreboard players set {NEW} rdHHit 0',
    f'scoreboard players set {NEW} mlv 1',
    f'execute if entity @e[tag=rlk_raiden,limit=1] run scoreboard players operation {NEW} mlv = @e[tag=rlk_raiden,limit=1] mlv',
    f'execute as {NEW} at @s rotated as @s run function {H}init',
    'tag @e[tag=rlk_rd_hnew] remove rlk_rd_hnew',
])
write('init', [
    '# @s = the new hazard at its origin. Clamp tell/life, cache the forward vector, number it, size it, decal it.',
    'scoreboard players operation @s rdWind > #rdOne rd',
    'scoreboard players operation @s rdHEv > #rdOne rd',
    'scoreboard players operation #rdMinLife rd = @s rdWind',
    'scoreboard players add #rdMinLife rd 10',
    'execute if score @s rdHK matches 5..7 run scoreboard players operation #rdMinLife rd = @s rdWind',
    'execute if score @s rdHK matches 5..7 run scoreboard players operation #rdMinLife rd += @s rdHF',
    'execute if score @s rdHK matches 5..7 run scoreboard players add #rdMinLife rd 2',
    'scoreboard players operation @s rdHLife > #rdMinLife rd',
    'execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_haxis","rlk_raiden_aux","rlk_room"]}',
    'execute store result score #rdOX rd run data get entity @s Pos[0] 1000',
    'execute store result score #rdOZ rd run data get entity @s Pos[2] 1000',
    '# S3 perf: the origin is cached (rdHOX/Y/Z, milliblocks); only the follow kind moves and refreshes it.',
    'scoreboard players operation @s rdHOX = #rdOX rd',
    'scoreboard players operation @s rdHOZ = #rdOZ rd',
    'execute store result score @s rdHOY run data get entity @s Pos[1] 1000',
    'execute store result score @s rdFX run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[0] 1000',
    'execute store result score @s rdFZ run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[2] 1000',
    'scoreboard players operation @s rdFX -= #rdOX rd',
    'scoreboard players operation @s rdFZ -= #rdOZ rd',
    'kill @e[tag=rlk_rd_haxis]',
    'scoreboard players add #rdHazardSerial rd 1',
    'scoreboard players operation @s rdHId = #rdHazardSerial rd',
    f'execute if score @s rdHK matches {KINDS["to_wall"]} run function {H}k/to_wall_len',
    'execute if score @s rdHGrp matches 1 run scoreboard players operation @s rdHGrp = #rdGrpSerial rd',
    'execute unless score @s rdHDk matches 1.. run tag @s add rlk_rd_quiet',
    f'execute if score @s rdHDk matches 1.. run function {H}vis/decal',
])

# to_wall: t = -b + sqrt(b^2 - (|p|^2 - R^2)), p = origin - arena centre, b = p.u (milliblocks); Newton square root.
R2 = int(24000 ** 2)
tw = ['# @s = a new to_wall hazard: length from the origin along its yaw to the arena wall circle (r 24), at most 47.',
      'scoreboard players set @s rdHA 47000',
      'execute unless entity @e[tag=rlk_raiden_arena,limit=1] run return 0',
      'execute store result score #rdPX rd run data get entity @s Pos[0] 1000',
      'execute store result score #rdPZ rd run data get entity @s Pos[2] 1000',
      'execute store result score #rdCX rd run data get entity @e[tag=rlk_raiden_arena,limit=1] Pos[0] 1000',
      'execute store result score #rdCZ rd run data get entity @e[tag=rlk_raiden_arena,limit=1] Pos[2] 1000',
      'scoreboard players operation #rdPX rd -= #rdCX rd',
      'scoreboard players operation #rdPZ rd -= #rdCZ rd',
      'scoreboard players operation #rdB rd = #rdPX rd',
      'scoreboard players operation #rdB rd *= @s rdFX',
      'scoreboard players operation #rdT rd = #rdPZ rd',
      'scoreboard players operation #rdT rd *= @s rdFZ',
      'scoreboard players operation #rdB rd += #rdT rd',
      'scoreboard players operation #rdB rd /= #rdK1000 rd',
      'scoreboard players operation #rdC rd = #rdPX rd',
      'scoreboard players operation #rdC rd *= #rdPX rd',
      'scoreboard players operation #rdT rd = #rdPZ rd',
      'scoreboard players operation #rdT rd *= #rdPZ rd',
      'scoreboard players operation #rdC rd += #rdT rd',
      f'scoreboard players set #rdT rd {R2}',
      'scoreboard players operation #rdC rd -= #rdT rd',
      'scoreboard players operation #rdDisc rd = #rdB rd',
      'scoreboard players operation #rdDisc rd *= #rdB rd',
      'scoreboard players operation #rdDisc rd -= #rdC rd',
      'execute unless score #rdDisc rd matches 1.. run return 0',
      'scoreboard players set #rdX rd 34000']
for _ in range(9):
    tw += ['scoreboard players operation #rdT rd = #rdDisc rd', 'scoreboard players operation #rdT rd /= #rdX rd',
           'scoreboard players operation #rdX rd += #rdT rd', 'scoreboard players operation #rdX rd /= #rdTwo rd']
tw = tw[:-36] + ['scoreboard players set #rdTwo rd 2'] + tw[-36:]
tw += ['scoreboard players operation #rdX rd -= #rdB rd',
       'execute if score #rdX rd matches 0..47000 run scoreboard players operation @s rdHA = #rdX rd',
       'execute if score #rdX rd matches ..-1 run scoreboard players set @s rdHA 0']
write('k/to_wall_len', tw)

# ------------------------------------------------------------------------------------------------ ticking
# (S3 perf: world runs tick_at directly, `execute as @e[tag=rlk_rd_hazard] at @s rotated as @s`; the old one-line
# hazard/tick wrapper is gone.)
write('tick_at', [
    '# World: as each hazard at its origin and frozen yaw. #rdRel = ticks since the hit / launch (negative before).',
    'scoreboard players add @s rdHAge 1',
    f'execute if score @s rdHAge >= @s rdHLife run return run function {H}expire',
    'scoreboard players operation #rdRel rd = @s rdHAge',
    'scoreboard players operation #rdRel rd -= @s rdWind',
    '# Travelling cards start to move gap ticks after their summon (rel rdHGo; raiden_kit.TRAVEL_GAP, user 10-22).',
    f'execute if score #rdRel rd = @s rdHGo if score @s rdHK matches 5..7 run function {H}vis/travel_go',
    '# S3-F perf (review RD-P1): a travelling hazard whose hit is spent (it hit, or its front passed the body) only',
    '# waits for its expiry (post: front past `reach`); its cards fly on by interpolation.',
    'execute if score @s rdHHit matches 1.. if score @s rdHMax matches 1.. if score @s rdHK matches 5..7 '
    'if score @s rdHHit >= @s rdHMax if score #rdRel rd <= @s rdHF run return 0',
    '# S3-F perf: a slab whose front is still well short of the body waits until it could reach it (k/slab_wait).',
    'execute if score @s rdHNx > @s rdHAge if score #rdRel rd <= @s rdHF run return 0',
    f'execute if score @s rdHK matches {KINDS["follow"]} run function {H}k/follow_move',
    f'execute if score #rdRel rd matches ..-1 run return run function {H}pre',
    f'execute if score #rdRel rd matches 0 run return run function {H}fire',
    f'function {H}post',
])
write('pre', [
    '# Before the hit: travelling cards appear at rel rdHSp (min(tell, gap) ticks before the launch); a decal with its',
    '# own life ends.',
    f'execute if score @s rdHK matches 5..7 if score #rdRel rd = @s rdHSp run function {H}vis/travel',
    f'execute if score @s rdHDl matches 1.. if score @s rdHAge = @s rdHDl run function {H}vis/decal_off',
])
write('fire', [
    '# The hit / launch tick: the decal goes, the strike visual comes (static kinds), the test runs.',
    f'execute if score @s rdHDk matches 1.. unless score @s rdHK matches 8..9 run function {H}vis/decal_off',
    f'execute if score @s rdHSv matches 1.. unless score @s rdHK matches 5..8 run function {H}vis/strike',
    f'execute if score @s rdHSnd matches 1.. unless score @s rdHK matches 5..9 run function {H}snd',
    f'function {H}try',
])
write('post', [
    '# After the hit: travelling hazards test every tick until their front passed `reach`; follow / field every rdHEv.',
    f'execute if score @s rdHK matches 5..7 if score #rdRel rd > @s rdHF run return run function {H}expire',
    f'execute if score @s rdHK matches 5..7 run return run function {H}try',
    f'execute if score @s rdHK matches 8..9 run function {H}try_every',
])
write('try_every', [
    'scoreboard players operation #rdMod rd = #rdRel rd',
    'scoreboard players operation #rdMod rd %= @s rdHEv',
    'execute unless score #rdMod rd matches 0 run return 0',
    f'function {H}try',
])
write('try', [
    'execute if score @s rdHMax matches 1.. if score @s rdHHit >= @s rdHMax run return 0',
    f'function {H}hit',
    f'execute if score #rdHit rd matches 1 run function {H}land',
])
write('snd', [
    'playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.5 1.25 0.2',
    'execute if score @s rdHSnd matches 2 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.55 1.4 0.25',
])
write('expire', [
    '# @s = the hazard (callers may run this `as` it from anywhere): remove it and its bound displays.',
    'scoreboard players operation #rdOwner rd = @s rdHId',
    'execute at @s as @e[tag=rlk_rd_hvis,distance=..0.05] if score @s rdVId = #rdOwner rd run kill @s',
    'kill @s',
])
write('finish', [
    '# Pattern end: every hazard that is not `detached` goes (travelling waves flagged detached run on).',
    'kill @e[tag=rlk_rd_hazard,tag=!rlk_rd_detached]',
    f'function {H}vfx_world',
])
write('clear', [
    '# Pause / transform / exhausted / death / cleanup: every hazard and every kit display.',
    'kill @e[tag=rlk_rd_hazard]',
    'kill @e[tag=rlk_rd_hvis]',
    'kill @e[tag=rlk_rd_fx]',
    'kill @e[tag=rlk_rd_sdecal]',
])

# follow: chase the player's feet horizontally at fv blocks per tick, never past them; the pool decal goes along.
write('k/follow_move', [
    '# @s = follow hazard. Horizontal chase (pitch 0) at data.fv blocks per tick; snaps when closer than one step.',
    'execute unless entity @e[tag=rlk_body,limit=1] run return 0',
    'execute store result score #rdT rd run data get entity @s data.fv 1000',
    'scoreboard players operation #rdPX rd = #rdBX rd',
    'scoreboard players operation #rdPZ rd = #rdBZ rd',
    'scoreboard players operation #rdPX rd -= @s rdHOX',
    'scoreboard players operation #rdPZ rd -= @s rdHOZ',
    'scoreboard players operation #rdR2 rd = #rdPX rd',
    'scoreboard players operation #rdR2 rd *= #rdPX rd',
    'scoreboard players operation #rdC rd = #rdPZ rd',
    'scoreboard players operation #rdC rd *= #rdPZ rd',
    'scoreboard players operation #rdR2 rd += #rdC rd',
    'scoreboard players operation #rdC rd = #rdT rd',
    'scoreboard players operation #rdC rd *= #rdT rd',
    f'execute if score #rdR2 rd <= #rdC rd at @e[tag=rlk_body,limit=1] run function {H}k/follow_snap',
    f'execute if score #rdR2 rd > #rdC rd facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function {H}k/follow_step with entity @s data',
    'scoreboard players operation #rdOwner rd = @s rdHId',
    'execute at @s as @e[tag=rlk_rd_hvis,distance=..3] if score @s rdVId = #rdOwner rd run tp @s ~ ~ ~',
    '# the cached origin follows the marker',
    'execute store result score @s rdHOX run data get entity @s Pos[0] 1000',
    'execute store result score @s rdHOY run data get entity @s Pos[1] 1000',
    'execute store result score @s rdHOZ run data get entity @s Pos[2] 1000',
])
write('k/follow_step', ['$tp @s ^ ^ ^$(fv)'])
write('k/follow_snap', [
    '# at the body: keep the hazard on its own floor height',
    'execute store result score #rdOY rd run data get entity @s Pos[1] 1000',
    'tp @s ~ ~ ~',
    'execute store result entity @s Pos[1] double 0.001 run scoreboard players get #rdOY rd',
])

# ------------------------------------------------------------------------------------------------ hit test
write('r2', [
    'scoreboard players operation #rdR2 rd = #rdDX rd',
    'scoreboard players operation #rdR2 rd *= #rdDX rd',
    'scoreboard players operation #rdT rd = #rdDZ rd',
    'scoreboard players operation #rdT rd *= #rdDZ rd',
    'scoreboard players operation #rdR2 rd += #rdT rd',
])
FS_FWD = ['scoreboard players operation #rdFwd rd = #rdDX rd',
          'scoreboard players operation #rdFwd rd *= @s rdFX',
          'scoreboard players operation #rdT rd = #rdDZ rd',
          'scoreboard players operation #rdT rd *= @s rdFZ',
          'scoreboard players operation #rdFwd rd += #rdT rd',
          'scoreboard players operation #rdFwd rd /= #rdK1000 rd']
FS_SIDE = ['scoreboard players operation #rdSide rd = #rdDX rd',
           'scoreboard players operation #rdSide rd *= @s rdFZ',
           'scoreboard players operation #rdT rd = #rdDZ rd',
           'scoreboard players operation #rdT rd *= @s rdFX',
           'scoreboard players operation #rdSide rd -= #rdT rd',
           'scoreboard players operation #rdSide rd /= #rdK1000 rd',
           'scoreboard players operation #rdAbsSide rd = #rdSide rd',
           'scoreboard players set #rdNeg rd -1',
           'execute if score #rdAbsSide rd matches ..-1 run scoreboard players operation #rdAbsSide rd *= #rdNeg rd']
write('fs', ['# Project onto the frozen forward and left axes (milliblocks).'] + FS_FWD + FS_SIDE)
K = KINDS
write('body', [
    '# World, once per tick before the hazards tick: the body (rlk_body) feet in milliblocks for hazard/hit.',
    'execute store result score #rdBX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000',
    'execute store result score #rdBY rd run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000',
    'execute store result score #rdBZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000',
])
write('hit', [
    '# @s = hazard at its origin. Body feet (rlk_body) relative to the origin; R2 only for radial kinds.',
    'scoreboard players set #rdHit rd 0',
    'execute unless entity @e[tag=rlk_body,distance=..46,limit=1] run return 0',
    '# S3 perf: the body position is read once per tick (hazard/body, from world) and the origin is cached at init.',
    'scoreboard players operation #rdDX rd = #rdBX rd',
    'scoreboard players operation #rdDZ rd = #rdBZ rd',
    'scoreboard players operation #rdDX rd -= @s rdHOX',
    'scoreboard players operation #rdDZ rd -= @s rdHOZ',
    f'execute unless score @s rdHK matches {K["rect"]}..{K["to_wall"]} unless score @s rdHK matches {K["slab"]}..{K["orb"]} run function {H}r2',
    f'execute if score @s rdHK matches {K["safe_dome"]} run return run function {H}k/safe_dome',
    'scoreboard players operation #rdDY rd = #rdBY rd',
    'scoreboard players operation #rdDY rd -= @s rdHOY',
    'execute unless score #rdDY rd matches -500..3500 run return 0',
    'execute if entity @s[tag=rlk_rd_jump] unless score #rdDY rd matches -500..750 run return 0',
    f'execute unless score @s rdHK matches 1 unless score @s rdHK matches 5..6 unless score @s rdHK matches 8..9 run function {H}fs',
    '# S3 perf: one dispatch line runs (travelling kinds first, they test every tick); `try` lands the hit.',
] + [f'execute if score @s rdHK matches {K[k]} run return run function {H}k/{k}'
     for k in ('slab', 'orb', 'sweep', 'disk', 'annulus', 'rect', 'follow', 'field')] + [
    f'execute if score @s rdHK matches {K["to_wall"]} run return run function {H}k/rect',
])
for k in ('disk', 'follow', 'field'):
    write(f'k/{k}', ['execute if score #rdR2 rd <= @s rdHE run scoreboard players set #rdHit rd 1'])
ANGLE = ['scoreboard players operation #rdT rd = #rdFwd rd',
         'scoreboard players operation #rdT rd *= @s {s}',
         'scoreboard players operation #rdT2 rd = #rdAbsSide rd',
         'scoreboard players operation #rdT2 rd *= @s {c}',
         'scoreboard players operation #rdT rd -= #rdT2 rd',
         'execute if score #rdT rd matches 0.. run scoreboard players set #rdHit rd 1']
write('k/annulus', [
    '# rmin - tol <= d <= r + tol and |angle| <= half  <=>  fwd*sin(half) - |side|*cos(half) >= 0 (any half 0..180).',
    'execute if score #rdR2 rd > @s rdHE run return 0',
    'execute if score #rdR2 rd < @s rdHF run return 0',
] + [a.format(s='rdHC', c='rdHD') for a in ANGLE])
write('k/rect', [
    '# off - tol <= forward <= off + len + tol and |side| <= half width + tol',
    'scoreboard players operation #rdLo rd = @s rdHC',
    'scoreboard players operation #rdLo rd -= @s rdHTol',
    'scoreboard players operation #rdHi rd = @s rdHC',
    'scoreboard players operation #rdHi rd += @s rdHA',
    'scoreboard players operation #rdHi rd += @s rdHTol',
    'scoreboard players operation #rdW rd = @s rdHB',
    'scoreboard players operation #rdW rd += @s rdHTol',
    'execute if score #rdFwd rd >= #rdLo rd if score #rdFwd rd <= #rdHi rd if score #rdAbsSide rd <= #rdW rd run scoreboard players set #rdHit rd 1',
])
FRONT = ['scoreboard players operation #rdF rd = #rdRel rd',
         'scoreboard players operation #rdF rd *= @s rdHB',
         'scoreboard players operation #rdF rd /= #rdK1000 rd',
         'scoreboard players operation #rdF rd += @s rdHA']
write('k/sweep', [
    '# Travelling arc: front F = r0 + v*t; band [F - band - tol, F + tol]; |angle| <= half (half 180: whole ring).',
] + FRONT + [
    'scoreboard players operation #rdHi rd = #rdF rd',
    'scoreboard players operation #rdHi rd += @s rdHTol',
    'scoreboard players operation #rdHi rd *= #rdHi rd',
    'execute if score #rdR2 rd > #rdHi rd run return 0',
    'scoreboard players operation #rdLo rd = #rdF rd',
    'scoreboard players operation #rdLo rd -= @s rdHC',
    'scoreboard players operation #rdLo rd -= @s rdHTol',
    'execute if score #rdLo rd matches ..-1 run scoreboard players set #rdLo rd 0',
    'scoreboard players operation #rdLo rd *= #rdLo rd',
    '# S3-F perf (review RD-P1): the front only moves outward, so once the body is behind the band this hazard can',
    '# never reach it: it is spent (rdHHit = rdHMax) and `try` skips it until it expires; its cards fly on.',
    'execute if score #rdR2 rd < #rdLo rd run return run scoreboard players operation @s rdHHit > @s rdHMax',
    'execute if score @s rdHE matches ..-999 run return run scoreboard players set #rdHit rd 1',
    'function %sfs' % H,
] + [a.format(s='rdHD', c='rdHE') for a in ANGLE])
write('k/slab', [
    '# Travelling straight front: F = d0 + v*t; forward in [F - depth - tol, F + tol], |side| <= w + tol.',
    '# S3 perf: the forward test comes first (hazard/hit skips fs for slabs), so the ticks while the front is away from',
    '# the body cost no side projection.',
] + FRONT + [
    'scoreboard players operation #rdHi rd = #rdF rd',
    'scoreboard players operation #rdHi rd += @s rdHTol',
    'scoreboard players operation #rdLo rd = #rdF rd',
    'scoreboard players operation #rdLo rd -= @s rdHD',
    'scoreboard players operation #rdLo rd -= @s rdHTol',
] + FS_FWD + [
    '# S3-F perf (review RD-P1): the front only moves outward, so once the body is behind the band this hazard can',
    '# never reach it: it is spent (rdHHit = rdHMax) and `try` skips it until it expires; its cards fly on.',
    'execute if score #rdFwd rd < #rdLo rd run return run scoreboard players operation @s rdHHit > @s rdHMax',
    'execute if score #rdFwd rd > #rdHi rd run return run function %sk/slab_wait' % H,
] + FS_SIDE + [
    'scoreboard players operation #rdW rd = @s rdHC',
    'scoreboard players operation #rdW rd += @s rdHTol',
    'execute if score #rdAbsSide rd <= #rdW rd run scoreboard players set #rdHit rd 1',
])
write('k/slab_wait', [
    '# S3-F perf: the body is ahead of the slab front by (#rdFwd - #rdHi) mb. The gap closes at most at v + 2 b/t (the',
    '# body dashing at it), so the slab skips its test until then (rdHNx = the age of the next test; tick_at).',
    'scoreboard players operation #rdGap rd = #rdFwd rd',
    'scoreboard players operation #rdGap rd -= #rdHi rd',
    'scoreboard players operation #rdCl rd = @s rdHB',
    'scoreboard players operation #rdCl rd /= #rdK1000 rd',
    'scoreboard players add #rdCl rd 2000',
    'scoreboard players operation #rdGap rd /= #rdCl rd',
    'scoreboard players operation @s rdHNx = @s rdHAge',
    'scoreboard players operation @s rdHNx += #rdGap rd',
])
write('k/orb', [
    '# Travelling disk: centre at forward F = d0 + v*t on the axis, radius r + tol (rdHD).',
] + FRONT + [
    'scoreboard players operation #rdQ rd = #rdFwd rd',
    'scoreboard players operation #rdQ rd -= #rdF rd',
    'execute if score #rdQ rd matches ..-1 run scoreboard players operation #rdQ rd *= #rdNeg rd',
    'execute if score #rdQ rd > @s rdHD run return 0',
    'execute if score #rdAbsSide rd > @s rdHD run return 0',
    'scoreboard players operation #rdQ rd *= #rdQ rd',
    'scoreboard players operation #rdT rd = #rdAbsSide rd',
    'scoreboard players operation #rdT rd *= #rdAbsSide rd',
    'scoreboard players operation #rdQ rd += #rdT rd',
    'scoreboard players operation #rdT rd = @s rdHD',
    'scoreboard players operation #rdT rd *= @s rdHD',
    'execute if score #rdQ rd <= #rdT rd run scoreboard players set #rdHit rd 1',
])
write('k/safe_dome', [
    '# 만겁: inside the dome (r, no pad) takes the hazard damage; anywhere else is fatal. Jumping does not help.',
    f'execute if score #rdR2 rd <= @s rdHE run return run function {H}land',
    'scoreboard players add @s rdHHit 1',
    f'execute as @a[tag=player,scores={{dead=0}},limit=1] run function {H}fatal',
])
write('fatal', [
    '# @s = player: the instant kill (dash i-frames and shields do not apply; Ronova revival still does).',
    'execute if score @s rnDie matches 1.. run return 0',
    'scoreboard players operation #hurtDmg tmp = @s curHealth',
    'scoreboard players set #elem tmp 3',
    'function rlk:player/hurt_do',
    'scoreboard players set @s curHealth 0',
    'function rlk:player/die',
])
write('land', [
    '# A hit (a dodge also consumes it). Group members share it; nododge ignores the dash i-frames.',
    'scoreboard players add @s rdHHit 1',
    f'execute if score @s rdHGrp matches 1.. run function {H}grp',
    'scoreboard players operation #cmDmg tmp = @s rdDamage',
    'scoreboard players operation #cmLv tmp = @s mlv',
    'scoreboard players set #cmEl tmp 3',
    'scoreboard players set #dodged tmp 0',
    f'execute if entity @s[tag=rlk_rd_nododge] run function {H}land_nd',
    'execute unless entity @s[tag=rlk_rd_nododge] run function rlk:boss/raiden/hurt',
    f'execute if score @s rdHKb matches 1.. unless score #dodged tmp matches 1 run function {H}kb',
    f'execute if score @s rdHK matches 5..9 at @e[tag=rlk_body,limit=1] run function {H}vis/impact',
])
write('land_nd', [
    '# Undodgeable (돌진, 수천수만의 염원, guard recovery): dash i-frames are 0 for this one hit, then restored.',
    'execute as @a[tag=player,limit=1] store result score #rdDI rd run scoreboard players get @s dashInvT',
    'scoreboard players set @a[tag=player,limit=1] dashInvT 0',
    'scoreboard players set #rdNoDodge rd 1',
    'function rlk:boss/raiden/hurt',
    'scoreboard players set #rdNoDodge rd 0',
    'scoreboard players operation @a[tag=player,limit=1] dashInvT = #rdDI rd',
])
write('grp', [
    'scoreboard players operation #rdG rd = @s rdHGrp',
    'execute as @e[tag=rlk_rd_hazard] if score @s rdHGrp = #rdG rd run scoreboard players operation @s rdHHit > @s rdHMax',
])
write('kb', [
    '# Knock-back through the engine push path (player/knockback: 0.1-block steps with block checks), away from the',
    '# hazard origin; #cmKB = rdHKb steps (k steps push 0.05 k (k+1) blocks). The engine stops it at the wall.',
    'kill @e[tag=rlk_plkb_source]',
    'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb_source","rlk_rd_kbsrc"]}',
    'execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 run tp @e[tag=rlk_rd_kbsrc,limit=1] ~ ~ ~ ~ 0',
    'scoreboard players operation #cmKB tmp = @s rdHKb',
    'execute as @a[tag=player,limit=1] run function rlk:player/knockback/start',
    'kill @e[tag=rlk_rd_kbsrc]',
])

from build_raiden_hazard_vfx import build as build_display_vfx
build_display_vfx(ROOT, OUT)
print(f"Generated the v2 hazard engine: {len(KINDS)} kinds, "
      f"{len(list(OUT.rglob('*.mcfunction')))} functions.")
