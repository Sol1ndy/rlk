# @s = body at the centre: a front with a 24 t charge (the hazard, the charge sphere at the
# core, the charge hiss; no ground decal: telegraph rule 10-20).
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:24,dmg:75}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
execute positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/p/wave_charge {t:24}
function rlk:mboss/fieldgen/fx/snd/wave_charge
