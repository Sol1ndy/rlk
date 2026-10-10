execute if score @s rdWalk matches 1.. run return run function rlk:boss/raiden/movement/walk_tick
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdAnim 0
execute if score @s rdPhase matches 0 at @s unless entity @e[tag=rlk_body,distance=..5] rotated as @s run function rlk:boss/raiden/approach
execute if score @s rdCool matches ..0 at @s run function rlk:boss/raiden/choose
