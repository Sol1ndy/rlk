# thrust clip tick 19
execute at @s rotated as @s rotated ~ 0 positioned ^-1.427 ^1.485 ^2.187 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-1.235 ^1.59 ^2.27 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-1.037 ^1.699 ^2.356 run particle minecraft:dust{color:[0.992f,0.957f,0.584f],scale:0.9} ~ ~ ~ 0.03 0.03 0.03 0 1 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p1c,limit=1] positioned ^ ^ ^3 run function rlk:mboss/mv/glide {t:2}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.9 0.23
