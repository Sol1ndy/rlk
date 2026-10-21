# As the boss with a chosen close-range pattern (rdGo 1..): the clock stays at 0.
scoreboard players set @s rdTime 0
scoreboard players add @s rdGo 1
execute if score @s rdBlink matches 1.. run return 0
# A blink taken because the dash was pinned or timed out: start where she landed.
execute if score @s rdGo matches 100.. run return run function rlk:boss/raiden/close_done
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdGo matches 2 at @s unless entity @e[tag=rlk_body,distance=..18] run return run function rlk:boss/raiden/movement/blink_start
scoreboard players set #rdNear rd 0
execute if score @s rdPat matches 1 at @s if entity @e[tag=rlk_body,distance=..4] run scoreboard players set #rdNear rd 1
execute if score @s rdPat matches 2 at @s if entity @e[tag=rlk_body,distance=..13] run scoreboard players set #rdNear rd 1
execute if score @s rdPat matches 11 at @s if entity @e[tag=rlk_body,distance=..4] run scoreboard players set #rdNear rd 1
execute if score @s rdPat matches 16 at @s if entity @e[tag=rlk_body,distance=..5] run scoreboard players set #rdNear rd 1
execute if score @s rdPat matches 19 at @s if entity @e[tag=rlk_body,distance=..10] run scoreboard players set #rdNear rd 1
execute if score #rdNear rd matches 1 run return run function rlk:boss/raiden/close_done
execute if score @s rdGo matches 45.. run return run function rlk:boss/raiden/close_blink
scoreboard players set @s rdAnim 21
scoreboard players set #rdStep rd 0
execute if score @s rdPhase matches 0 at @s rotated as @s positioned ^ ^ ^0.55 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] store success score #rdStep rd run tp @s ~ ~ ~
execute if score @s rdPhase matches 2 at @s rotated as @s positioned ^ ^ ^0.65 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] store success score #rdStep rd run tp @s ~ ~ ~
# Pinned (the straight line to the player leaves the arena disc, or a block is in the way).
execute if score #rdStep rd matches 0 run return run function rlk:boss/raiden/close_blink
execute if score @s rdGo matches 3 at @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.5 1.3 0.2
