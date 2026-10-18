# B2 tick: the crescents fly first (the module tick runs before mv and pj move them next tick).
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p12c,limit=1] run function rlk:mboss/butterfly/p/barrage/fly
execute if score #bfPT mb matches -4..56 run return run function rlk:mboss/butterfly/p/barrage/d/m4_56
execute if score #bfPT mb matches 57..117 run return run function rlk:mboss/butterfly/p/barrage/d/57_117
