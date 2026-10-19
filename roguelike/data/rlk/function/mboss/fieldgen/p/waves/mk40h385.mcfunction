# @s = body: the 40 t front of the closing 3rd wave, its charge sphere at 3.85 b (the sinking core).
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:40,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
function rlk:mboss/fieldgen/fx/tele/wave {r0:25,r1:212,w:25,tell:40,dur:34,el:9,hold:2}
execute positioned ~ ~3.85 ~ run function rlk:mboss/fieldgen/fx/p/wave_charge {t:40}
function rlk:mboss/fieldgen/fx/snd/wave_charge
