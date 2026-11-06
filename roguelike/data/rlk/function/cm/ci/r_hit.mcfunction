scoreboard players set #cmDmg tmp 8
scoreboard players set #cmEl tmp 3
scoreboard players operation #cmLv tmp = @s mlv
function rlk:cm/hit_pl
execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.3 0.3 0.3 0.1 12
function rlk:cm/ci/r_end
