scoreboard players set @s c2T2 1
scoreboard players set #c3FuHit tmp 1
particle minecraft:composter ~ ~0.9 ~ 0.4 0.3 0.4 0.1 10 normal
scoreboard players operation #cmDmg tmp = #c3D_fu tmp
function rlk:cm/hit_me
