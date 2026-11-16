# One step of the move #ai_mv (@s = body; the recovery, a pattern's kept tail): walk / glide in (stop at 3 b), the far
# fallback's glide, strafe left / right, the backstep (straight away from the player while nearer than 5 b,
# its first 10 t); every step mv/ok-checked.
execute if score #ai_mv hr matches 1 at @s unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/toward {d:0.12}
execute if score #ai_mv hr matches 5 at @s unless entity @e[tag=rlk_body,limit=1,distance=..3] run function rlk:mboss/mv/toward {d:0.18}
execute if score #ai_mv hr matches 4 at @s unless entity @e[tag=rlk_body,limit=1,distance=..8] run function rlk:mboss/mv/toward {d:0.3}
execute if score #ai_mv hr matches 4 at @s if entity @e[tag=rlk_body,limit=1,distance=..8] run scoreboard players set #rec hr 0
execute if score #ai_mv hr matches 7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..4] run function rlk:mboss/mv/toward {d:0.3}
execute if score #ai_mv hr matches 7 at @s if entity @e[tag=rlk_body,limit=1,distance=..4] run scoreboard players set #rec hr 0
execute if score #ai_mv hr matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.12 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #ai_mv hr matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.12 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #ai_mv hr matches 6 if score #rec hr matches 2.. at @s if entity @e[tag=rlk_body,limit=1,distance=..5] facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^0.3 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
