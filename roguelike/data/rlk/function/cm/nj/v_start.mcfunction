scoreboard players set @s cmS 1
scoreboard players set @s cmT 8
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
particle minecraft:large_smoke ~ ~1 ~ 0.35 0.6 0.35 0.02 24
particle minecraft:poof ~ ~1 ~ 0.4 0.6 0.4 0.03 16
playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 1 1.3
