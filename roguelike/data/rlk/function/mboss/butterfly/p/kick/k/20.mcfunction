# kick clock 20
execute if score #bp1S mb matches 0 run execute at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute unless score #bp1S mb matches 0 run execute at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
