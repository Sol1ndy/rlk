# @s = body: an extra front of the triple 3rd wave (tell 10): the hazard and its sound (the charge pulse
# is on the timeline, at the core's height of that variant: fix round FID-7; no ground decal).
scoreboard players set #hzAct mb 36
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzY1 mb 7
function rlk:mboss/hz/ring {r0:0,r:25,tell:10,dmg:75}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p21f
function rlk:mboss/fieldgen/fx/snd/wave_charge2
