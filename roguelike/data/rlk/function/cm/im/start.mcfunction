scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #cmW_im tmp
function rlk:cm/ch_begin
execute unless score #k79 snd matches 1 run function rlk:snd/f85
