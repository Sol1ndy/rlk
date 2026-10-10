execute unless score @s rdWalk matches 1.. run return 0
execute if score @s rdBlink matches 1.. run return 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute if score @s rdWalkDir matches 0 at @s rotated as @s rotated ~70 0 run tp @s ~ ~ ~ ~ 0
execute if score @s rdWalkDir matches 1 at @s rotated as @s rotated ~-70 0 run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdAnim 1
execute at @s rotated as @s positioned ^ ^ ^0.11 if entity @e[tag=rlk_raiden_arena,distance=..20,limit=1] if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air run tp @s ~ ~ ~
execute if score @s rdPhase matches 0 if score @s rdWalk matches 9 at @s run playsound minecraft:block.stone.step hostile @a[tag=player] ~ ~ ~ 0.35 0.85 0.05
execute if score @s rdPhase matches 0 if score @s rdWalk matches 3 at @s run playsound minecraft:block.stone.step hostile @a[tag=player] ~ ~ ~ 0.3 0.95 0.05
scoreboard players remove @s rdWalk 1
execute if score @s rdWalk matches 0 run scoreboard players set @s rdAnim 0
