scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:electric_spark ~ ~0.5 ~ 0.15 0.15 0.15 0.02 2
execute if score @s cmT matches ..0 run function rlk:cm/ci/r_go
