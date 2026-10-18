# bomb tick.
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p1b] at @s run function rlk:mboss/fieldgen/p/bomb/bomb
execute if score #fgPT mb matches 8..36 run return run function rlk:mboss/fieldgen/p/bomb/d/8_36
execute if score #fgPT mb matches 37..100 run return run function rlk:mboss/fieldgen/p/bomb/d/37_100
