scoreboard players set @s cmS 1
scoreboard players set @s cmT 10
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 0.7 0.15 0.7 0 30
playsound minecraft:entity.warden.dig master @a ~ ~ ~ 0.9 1.5
