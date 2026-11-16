function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 422
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
function rlk:mboss/hz/disc {r:16,tell:12,dmg:44}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p42
