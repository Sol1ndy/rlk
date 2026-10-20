# slide #azPT 199
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w6]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 8
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:40,tell:20,dmg:100}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p20w6
data modify storage rlk:mboss az.tl set value {id:5,r0:40,r1:300,w:45,tell:20,dur:7,nd:2,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/fx/tele/wave with storage rlk:mboss az.tl
function rlk:mboss/line/say {t:"대지의 진노는 잠재울 수 없다!",c:"#F2B53A",gap:2,hold:50,snd:2}
