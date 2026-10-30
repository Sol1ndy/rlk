# thrust clip tick 39
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.3 1.9 0.1
execute at @s rotated as @s rotated ~ 0 positioned ^-0.553 ^3.185 ^1.329 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.605 ^2.31 ^1.753 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.647 ^1.581 ^2.106 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
