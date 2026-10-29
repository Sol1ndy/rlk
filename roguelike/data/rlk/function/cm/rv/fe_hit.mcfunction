scoreboard players set #cmDmg tmp 7
scoreboard players set #cmEl tmp 1
scoreboard players operation #cmLv tmp = @s cmLv
function rlk:cm/hit_pl
particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 8
kill @s
