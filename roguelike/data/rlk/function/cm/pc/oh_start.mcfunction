# overheated: 30 t in place, core exposed (rlk_c3_core: every hit x1.5), stunnable (the punish window)
scoreboard players set @s cmS 7
scoreboard players set @s cmT 30
scoreboard players set @s cmN 0
tag @s add rlk_c3_core
tag @s remove rlk_cmch
tag @s remove rlk_c2_fix
particle minecraft:cloud ~ ~1.6 ~ 0.4 0.4 0.4 0.05 12
particle minecraft:lava ~ ~1.5 ~ 0.3 0.3 0.3 0 4
playsound minecraft:block.fire.extinguish master @a ~ ~ ~ 1 0.6
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 0.9 0.7
