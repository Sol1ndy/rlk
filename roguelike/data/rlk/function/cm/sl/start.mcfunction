scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_sl tmp
scoreboard players operation @s cmCd = #c2Cd_sl tmp
particle minecraft:electric_spark ~ ~0.6 ~ 0.5 0.3 0.5 0.1 12 normal
execute unless score #c2slsquish snd matches 1 run function rlk:cm/c2/snd/slsquish
execute unless score #c2slcharge snd matches 1 run function rlk:cm/c2/snd/slcharge
