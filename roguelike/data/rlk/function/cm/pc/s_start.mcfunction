scoreboard players set @s cmS 1
scoreboard players set @s cmT 8
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.6 0.6 0.08 16
particle minecraft:block{block_state:"minecraft:smooth_quartz"} ~ ~1.4 ~ 0.6 0.6 0.6 0 16
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 0.8 1.6
playsound minecraft:block.stone.break master @a ~ ~ ~ 1 0.8
