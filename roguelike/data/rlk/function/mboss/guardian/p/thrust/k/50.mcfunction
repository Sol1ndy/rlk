# thrust clip tick 50
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.3 1.9 0.3
execute at @s rotated as @s rotated ~ 0 positioned ^-0.538 ^3.221 ^1.327 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.582 ^2.346 ^1.752 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.618 ^1.617 ^2.105 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
