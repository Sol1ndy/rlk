# the first cast of the fight: the blast never kills (plan Q3).
scoreboard players set #hzAct mb 20
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzPm mb 800
scoreboard players set #hzPmL mb 0
scoreboard players operation #hzSafeG mb = #apq32G mb
scoreboard players set #hzR0 mb 45
function rlk:mboss/hz/mask {tell:116,dmg:1}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p32h
