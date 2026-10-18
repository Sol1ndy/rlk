# kick clock 30
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.7} ^-0.5 ^0.15 ^0.2 0.1 0.1 0.1 0 2 force @a[tag=player]
execute if score #bp1S mb matches 1 run execute at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute unless score #bp1S mb matches 1 run execute at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
