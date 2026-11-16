# One idle tick (@s = body, #pat 0): face the player, walk / strafe, then the decision when the recovery ran out.
execute if score #rec kn matches 1.. run scoreboard players remove #rec kn 1
function rlk:mboss/mv/turn {max:10}
execute if score #ai_mv kn matches 1 at @s unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/toward {d:0.12}
execute if score #ai_mv kn matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #ai_mv kn matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #rec kn matches ..0 run function rlk:boss/arlecchino/ai/decide
