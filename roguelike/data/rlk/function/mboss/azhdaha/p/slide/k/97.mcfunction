# slide #azPT 97
function rlk:mboss/azhdaha/kstub/snd/slide_wave
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w2]
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
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p20w2
data modify storage rlk:mboss az.tl set value {id:1,r0:40,r1:180,w:35,tell:20,dur:5,nd:2,hold:3}
execute store result storage rlk:mboss az.tl.el int 1 run scoreboard players get #azE mb
function rlk:mboss/azhdaha/kstub/tele/wave
execute if score #azTrN mb matches ..1 run function rlk:mboss/line/say {t:"천 년의 원한을 어찌 갚을까!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azTrN mb matches 2 run function rlk:mboss/line/say {t:"오늘이야말로 묵은 원한을 전부 청산하지!",c:"#F2B53A",gap:2,hold:50,snd:2}
