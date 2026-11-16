# Re-aim a live hazard (@s = its marker): it moves to the execution position and turns to the execution yaw
# (pitch ignored); the frozen forward axis of the hit test is recomputed exactly as hz/init does. For sweeping
# lines (lasers): execute as <marker> at <body> rotated as @s rotated ~5 0 positioned ^ ^ ^2.8 run function
# rlk:mboss/hz/aim. Call it from the module tick (it runs before hz/all, so this tick's hit test uses the new aim).
tp @s ~ ~ ~ ~ 0
execute at @s rotated as @s positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_hzax"]}
execute store result score #ox mb run data get entity @s Pos[0] 1000
execute store result score #oz mb run data get entity @s Pos[2] 1000
execute store result score @s mbHzFX run data get entity @e[type=minecraft:marker,tag=rlk_mb_hzax,limit=1] Pos[0] 1000
execute store result score @s mbHzFZ run data get entity @e[type=minecraft:marker,tag=rlk_mb_hzax,limit=1] Pos[2] 1000
scoreboard players operation @s mbHzFX -= #ox mb
scoreboard players operation @s mbHzFZ -= #oz mb
kill @e[type=minecraft:marker,tag=rlk_mb_hzax]
