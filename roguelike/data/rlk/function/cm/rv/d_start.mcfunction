scoreboard players set @s cmS 1
scoreboard players set @s cmT 10
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
playsound minecraft:entity.phantom.ambient master @a ~ ~ ~ 1 0.6
playsound minecraft:entity.ravager.roar master @a ~ ~ ~ 0.5 1.8
particle minecraft:flame ~ ~1 ~ 0.6 0.3 0.6 0.02 10
