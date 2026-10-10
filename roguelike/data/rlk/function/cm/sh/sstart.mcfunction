scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_sh tmp
scoreboard players operation @s cmCd = #cmCd_sh tmp
function rlk:cm/pose_c
execute unless score #k101 snd matches 1 run function rlk:snd/f108
