scoreboard players set @s rdAnim 1
execute rotated as @s positioned ^ ^ ^0.17 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~
