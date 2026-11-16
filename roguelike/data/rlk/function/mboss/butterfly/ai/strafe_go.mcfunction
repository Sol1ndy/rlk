execute unless score #bfMv mb matches 3 run function rlk:mboss/butterfly/ai/mv3
execute if score #bfSide mb matches 1 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~90 0 positioned ^ ^ ^0.1 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute if score #bfSide mb matches -1 run execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~-90 0 positioned ^ ^ ^0.1 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
