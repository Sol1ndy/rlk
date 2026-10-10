scoreboard players set @s cmS 2
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_shR tmp
function rlk:cm/ch_begin
function rlk:cm/pose_c
particle minecraft:angry_villager ~ ~2.6 ~ 0.2 0.1 0.2 0 2
execute unless score #k95 snd matches 1 run function rlk:snd/f102
