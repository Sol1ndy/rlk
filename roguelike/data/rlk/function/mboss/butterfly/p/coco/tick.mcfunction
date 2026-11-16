# B4 tick: the orbs steer (pj props; the module tick runs before pj/all moves them).
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p14o,limit=1] as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14o] at @s run function rlk:mboss/butterfly/p/coco/orb
execute if score #bfPT mb matches 65.. unless entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p14o,limit=1] run return run function rlk:mboss/butterfly/p/end
execute if score #bfPT mb matches 1..43 run return run function rlk:mboss/butterfly/p/coco/d/1_43
execute if score #bfPT mb matches 44..86 run return run function rlk:mboss/butterfly/p/coco/d/44_86
