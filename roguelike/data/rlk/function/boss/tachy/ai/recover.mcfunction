# One idle tick (@s = body, #pat 0): prowl, then the decision when the recovery ran out.
execute if score #rec tk matches 1.. run scoreboard players remove #rec tk 1
function rlk:mboss/mv/turn {max:8}
execute if score #ai_mv tk matches 1 at @s unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run function rlk:mboss/mv/toward {d:0.12}
execute if score #ai_mv tk matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #ai_mv tk matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #rec tk matches ..0 run function rlk:boss/tachy/ai/decide
