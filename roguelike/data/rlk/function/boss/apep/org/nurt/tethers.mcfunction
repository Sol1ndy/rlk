# @s = a linked 양육 (every 8 t, within the dust's 7-36 t life: the command budget at the cap, plan 7.6.4): a wavy
# tether from its orb to each of its
# basics (kit tether, len = the distance).
scoreboard players operation #apX mb = @s apL
tag @s add rlk_mb_ap_me
execute store result score #apNX mb run data get entity @s Pos[0] 10
execute store result score #apNZ mb run data get entity @s Pos[2] 10
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_buff] if score @s apL = #apX mb at @e[type=minecraft:husk,tag=rlk_mb_ap_me,limit=1] positioned ~ ~2.0 ~ facing entity @s feet run function rlk:boss/apep/org/nurt/tether1
tag @s remove rlk_mb_ap_me
