# Clock 25..156 (@s = body): beam A turns +5, beam B -5 degrees; the beam particles every 2 t.
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~5 0 positioned ^ ^ ^2.8 run function rlk:mboss/hz/aim
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~-5 0 positioned ^ ^ ^2.8 run function rlk:mboss/hz/aim
scoreboard players operation #fgM mb = #fgPT mb
scoreboard players operation #fgM mb %= #fgK2 mb
execute if score #fgM mb matches 0 as @e[type=minecraft:marker,tag=rlk_mb_fg_p3a,limit=1] at @s rotated as @s run function rlk:mboss/fieldgen/p/laser/beam
execute if score #fgM mb matches 0 as @e[type=minecraft:marker,tag=rlk_mb_fg_p3b,limit=1] at @s rotated as @s run function rlk:mboss/fieldgen/p/laser/beam
