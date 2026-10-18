# @s = body: the 20th count broke the field (역장 붕괴). Every threat goes (hazards, props, pulls, glides:
# lib_clear; the running pattern, waves included: p/cancel), the meter / low gravity / the damage cut end, the
# field state ends; the break plays (40 t: bubble, burst at 5, tilt, wobble, sink), then groggy 200 t.
# The kit: every decal goes (tele/clear), the banner if it still shows, the meter / low-gravity icon / hint
# (field/drop -> hud/kit_off); " · 그로기" on the name line from here to the end of the recovery.
scoreboard players set #fgBrkQ mb 0
function rlk:mboss/lib_clear
function rlk:mboss/fieldgen/p/cancel
function rlk:mboss/fieldgen/fx/tele/clear
function rlk:mboss/fieldgen/hud/banner_cut
function rlk:mboss/fieldgen/field/drop
function rlk:mboss/fieldgen/hud/groggy_on
# #fgT -1: the AI state runs brk/tick later this same tick, so #fgT = the break clip tick
scoreboard players set #fgSt mb 6
scoreboard players set #fgT mb -1
scoreboard players set #fgMv mb 0
function rlk:mboss/fieldgen/rig/play/break
function rlk:mboss/line/say {t:"역장 붕괴",c:"#FFE7A0",gap:2,hold:40,snd:2}
function rlk:mboss/fieldgen/seq_f/brk/start
function rlk:mboss/fieldgen/hud/refresh
