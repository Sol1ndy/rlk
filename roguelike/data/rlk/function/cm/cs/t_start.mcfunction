scoreboard players set @s cmS 8
scoreboard players set @s cmT 16
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
playsound minecraft:block.respawn_anchor.charge master @a ~ ~ ~ 0.9 1.5
playsound minecraft:entity.spider.ambient master @a ~ ~ ~ 0.6 0.5
