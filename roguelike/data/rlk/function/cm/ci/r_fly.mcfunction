scoreboard players operation @s cmT -= #eStep tmp
scoreboard players set #c2s tmp 2
function rlk:cm/ci/r_step
execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.05 0.05 0.05 0 2
execute if score @s cmS matches 2 if score @s cmT matches ..0 run function rlk:cm/ci/r_end
