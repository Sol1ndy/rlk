# thrust clip tick 56
execute at @s rotated as @s rotated ~ 0 positioned ^-0.723 ^2.899 ^1.801 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.959 ^2.16 ^2.39 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-1.156 ^1.545 ^2.881 run particle minecraft:dust{color:[0.988f,0.961f,0.682f],scale:0.7} ~ ~ ~ 0.04 0.04 0.04 0 1 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p1d,limit=1] positioned ^ ^ ^5 run function rlk:mboss/mv/glide {t:2}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.85 0.7 0.28
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
