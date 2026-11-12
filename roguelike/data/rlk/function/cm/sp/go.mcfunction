scoreboard players set @s cmS 2
scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
tag @s add rlk_cmch
execute unless score #c2spthrust snd matches 1 run function rlk:cm/c2/snd/spthrust
