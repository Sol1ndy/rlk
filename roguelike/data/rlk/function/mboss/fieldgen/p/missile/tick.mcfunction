# missile tick.
execute if score #fq4Pz mb matches 1 run function rlk:mboss/fieldgen/p/missile/resume
execute if score #fgPT mb matches 1..20 run function rlk:mboss/fieldgen/rig_stub/face/track
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p4m] at @s run function rlk:mboss/fieldgen/p/missile/age
execute if score #fgPT mb matches 4..27 run return run function rlk:mboss/fieldgen/p/missile/d/4_27
execute if score #fgPT mb matches 28..70 run return run function rlk:mboss/fieldgen/p/missile/d/28_70
