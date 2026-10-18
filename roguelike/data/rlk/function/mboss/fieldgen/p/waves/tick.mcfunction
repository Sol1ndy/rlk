# waves tick.
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p21f] run function rlk:mboss/fieldgen/p/waves/grow
execute if score #fgPT mb matches 2..90 run return run function rlk:mboss/fieldgen/p/waves/d/2_90
execute if score #fgPT mb matches 92..232 run return run function rlk:mboss/fieldgen/p/waves/d/92_232
