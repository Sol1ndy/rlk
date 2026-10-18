# B2 tick: the crescents fly first (the module tick runs before mv and pj move them next tick).
execute if entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p12c,limit=1] run function rlk:mboss/butterfly/p/barrage/fly
execute if score #bfPT mb matches 117.. unless entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p12c,limit=1] unless entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12t,limit=1] run return run function rlk:mboss/butterfly/p/end
execute if score #bfPT mb matches 1..58 run return run function rlk:mboss/butterfly/p/barrage/d/1_58
execute if score #bfPT mb matches 59..116 run return run function rlk:mboss/butterfly/p/barrage/d/59_116
