# kick clock 22
execute if score #bp1S mb matches 1 run execute at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
execute unless score #bp1S mb matches 1 run execute at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.25 if function rlk:mboss/mv/ok run tp @s ~ ~ ~
particle minecraft:poof ~ ~0.1 ~ 0.3 0.02 0.3 0.02 3 force @a[tag=player]
playsound minecraft:block.moss_carpet.step hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
