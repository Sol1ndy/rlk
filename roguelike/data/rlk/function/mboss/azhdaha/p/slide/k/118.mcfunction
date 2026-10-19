# slide #azPT 118
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p20w2] run function rlk:mboss/hz/resize {r:70,r0:35,w:0}
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w3]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 6
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:40,tell:20,dmg:80}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p20w3
data modify storage rlk:mboss az.tl set value {id:2,r0:40,r1:180,w:35,tell:20,dur:5,nd:2,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/kstub/tele/wave
