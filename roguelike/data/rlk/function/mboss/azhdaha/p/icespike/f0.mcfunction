# Positioned at F1: the star seal (keep) and its burst disc r 4.0, tell 42, own group.
function rlk:mboss/azhdaha/fx/tele/starseal_o {r:40,tell:42,el:4,hold:3}
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 451
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
function rlk:mboss/hz/disc {r:40,tell:42,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p45
