scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_fm tmp
scoreboard players set @s cmN 0
function rlk:cm/ch_begin
execute unless score #k88 snd matches 1 run function rlk:snd/f95
