# One idle tick (@s = body, #pat 0): face the player, walk / glide / strafe (mv/ok-checked), the flinch (6 t, no step),
# then the decision when the recovery ran out.
execute if score #rec hr matches 1.. run scoreboard players remove #rec hr 1
function rlk:mboss/mv/turn {max:10}
execute if score #ai_fl hr matches 1.. run scoreboard players remove #ai_fl hr 1
execute if score #ai_fl hr matches 1.. run return 0
execute if score #ai_mv hr matches 1 at @s unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/toward {d:0.12}
execute if score #ai_mv hr matches 5 at @s unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/toward {d:0.18}
execute if score #ai_mv hr matches 4 at @s unless entity @e[tag=rlk_body,limit=1,distance=..8] run function rlk:mboss/mv/toward {d:0.3}
execute if score #ai_mv hr matches 4 at @s if entity @e[tag=rlk_body,limit=1,distance=..8] run scoreboard players set #rec hr 0
execute if score #ai_mv hr matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.12 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #ai_mv hr matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.12 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #rec hr matches ..0 run function rlk:boss/scarlet/ai/decide
