# missile tick.
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p4m] at @s run function rlk:mboss/fieldgen/p/missile/age
execute if score #fgPT mb matches 2..20 run return run function rlk:mboss/fieldgen/p/missile/d/2_20
execute if score #fgPT mb matches 21..70 run return run function rlk:mboss/fieldgen/p/missile/d/21_70
