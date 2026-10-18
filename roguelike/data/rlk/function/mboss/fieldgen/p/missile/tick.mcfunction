# missile tick.
execute if score #fq4Pz mb matches 1 run function rlk:mboss/fieldgen/p/missile/resume
execute if score #fgPT mb matches 1..22 run function rlk:mboss/fieldgen/rig/face/track
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p4m] at @s run function rlk:mboss/fieldgen/p/missile/age
execute if score #fgPT mb matches 4..28 run return run function rlk:mboss/fieldgen/p/missile/d/4_28
execute if score #fgPT mb matches 29..66 run return run function rlk:mboss/fieldgen/p/missile/d/29_66
