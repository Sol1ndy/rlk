# stomp w #azPT 33
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p5w2] run function rlk:mboss/hz/resize {r:35,r0:15,w:0}
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p5w3]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 13
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:15,tell:14,dmg:90}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5w3
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p5w3,limit=1] mb 2000
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p5h
scoreboard players operation #aq5G3 mb = #mbGrp mb
