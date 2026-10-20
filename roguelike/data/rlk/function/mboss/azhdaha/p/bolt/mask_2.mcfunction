# Positioned at the arena centre: the mask hazard (kind 6) r0 3.2, tell 48, own group, its own
# safe group (#hzSafeG 0); the new circles become its safe markers (mbHzSG = #hzLast).
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 421
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzSafeG mb 0
scoreboard players set #hzY0 mb 0
scoreboard players set #hzY1 mb 30
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
scoreboard players set #hzR0 mb 32
function rlk:mboss/hz/mask {tell:48,dmg:120}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p42
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42n] run scoreboard players operation @s mbHzSG = #hzLast mb
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42n] add rlk_mb_hzsafe
