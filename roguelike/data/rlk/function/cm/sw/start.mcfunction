scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_sw tmp
scoreboard players operation @s cmCd = #cmCd_sw tmp
function rlk:cm/pose_c
execute unless score #k103 snd matches 1 run function rlk:snd/f110
