execute unless entity @e[tag=rlk_body,distance=..5] facing entity @e[tag=rlk_body,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.15}
execute if entity @e[tag=rlk_body,distance=..3] facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:mboss/mv/step_flat {spd:0.15}
execute if entity @e[tag=rlk_body,distance=3..5] facing entity @e[tag=rlk_body,limit=1] feet rotated ~90 0 run function rlk:mboss/mv/step_flat {spd:0.15}
function rlk:boss/apep/org/basic/push_in
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
function rlk:boss/apep/org/pred/swim_snd
