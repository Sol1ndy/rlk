# Positioned at F3: the star seal (keep) and its burst disc r 4.0, tell 54, own group (or the
# group of a field it overlaps after the wall clamp: FIX FAIR-8).
function rlk:boss/azhdaha/fx/tele/starseal_o {r:40,tell:54,el:4,hold:3}
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 451
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute if score #aq45M2 mb matches 1 run scoreboard players operation #hzGrp mb = #aq45G0 mb
execute if score #aq45M2 mb matches 2 run scoreboard players operation #hzGrp mb = #aq45G1 mb
scoreboard players operation #aq45G2 mb = #hzGrp mb
function rlk:mboss/hz/disc {r:40,tell:54,dmg:40}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p45
