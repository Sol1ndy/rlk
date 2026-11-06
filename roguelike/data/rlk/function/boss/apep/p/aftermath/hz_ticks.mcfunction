# B0 (fix 10-22f): the field ticks, 10 per mille of max HP, never lethal, re-armed every 10 t from
# #apPT 20 (the field at r 26.0) to the last tick before the blast (#apPT #apq32S + 155):
# #hzAct = #apq32S + 136; 15-20 ticks for a player outside every dome the whole time.
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzRearm mb 10
scoreboard players set #hzNR mb 1
scoreboard players set #hzPm mb 10
scoreboard players set #hzPmL mb 0
scoreboard players operation #hzAct mb = #apq32S mb
scoreboard players add #hzAct mb 136
scoreboard players operation #hzSafeG mb = #apq32G mb
scoreboard players set #hzR0 mb 45
function rlk:mboss/hz/mask {tell:20,dmg:1}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p32h
