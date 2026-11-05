# A8 pattern tick 102.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.35 0.7 0.35 0.02 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:end_rod ~ ~ ~ 0.25 0.6 0.25 0.04 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~75 0 positioned ^ ^ ^4.4 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
