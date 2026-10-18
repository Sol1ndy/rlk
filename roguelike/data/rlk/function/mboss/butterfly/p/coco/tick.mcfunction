# B4 tick: the orbs steer (they are pj props; the module tick runs before pj/all).
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p14o,limit=1] as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14o] at @s run function rlk:mboss/butterfly/p/coco/orb
execute if score #bfPT mb matches 19 run return run function rlk:mboss/butterfly/p/coco/k/19
execute if score #bfPT mb matches 46 run return run function rlk:mboss/butterfly/p/coco/k/46
execute if score #bfPT mb matches 98 run return run function rlk:mboss/butterfly/p/coco/k/98
