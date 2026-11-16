scoreboard players set @s cmS 3
scoreboard players set @s cmT 4
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 20
playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 1 1.6
