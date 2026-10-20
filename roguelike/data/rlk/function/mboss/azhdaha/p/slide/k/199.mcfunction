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
playsound minecraft:entity.ravager.roar hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
playsound minecraft:entity.ender_dragon.growl hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
function rlk:mboss/line/say {t:"대지의 진노는 잠재울 수 없다!",c:"#F2B53A",gap:2,hold:50,snd:2}
