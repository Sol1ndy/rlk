scoreboard players operation @s cmT -= #eStep tmp
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 run particle minecraft:flame ^1.6 ^1.1 ^0.4 0.1 0.1 0.1 0.01 2
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 run particle minecraft:flame ^-1.6 ^1.1 ^0.4 0.1 0.1 0.1 0.01 2
execute if score @s cmT matches ..0 run function rlk:cm/rv/f_throw
