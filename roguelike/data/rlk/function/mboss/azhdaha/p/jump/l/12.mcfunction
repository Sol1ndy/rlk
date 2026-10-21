# jump l at tick 12 (positioned / rotated at rlk_mb_az_p2l)
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p2w1]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 6
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:30,tell:20,dmg:44}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p2w1
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p2w1,limit=1] mb 1500
scoreboard players operation #aq2G2 mb = #mbGrp mb
