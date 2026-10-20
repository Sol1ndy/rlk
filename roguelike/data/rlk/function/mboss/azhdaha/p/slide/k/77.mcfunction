# slide #azPT 77
scoreboard players set #azNoPush mb 1
function rlk:mboss/azhdaha/rig/face/track
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w1]
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
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p20w1
data modify storage rlk:mboss az.tl set value {id:0,r0:40,r1:180,w:35,tell:20,dur:5,nd:2,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/fx/tele/wave with storage rlk:mboss az.tl
