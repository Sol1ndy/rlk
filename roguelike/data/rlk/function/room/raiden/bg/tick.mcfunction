# One backdrop slice per tick (20 slices: 43,935 blocks, then the panels).
# Stops when the boss map is gone (the zone 1 marker carries rlk_rd_bgzone) and waits for unloaded chunks.
execute unless entity @e[type=minecraft:marker,tag=rlk_rd_bgzone,limit=1] run return run scoreboard players set #rdBgI rd -1
execute in minecraft:overworld unless loaded -62 200 -62 run return run function rlk:room/raiden/bg/wait
execute in minecraft:overworld unless loaded 61 200 -62 run return run function rlk:room/raiden/bg/wait
execute in minecraft:overworld unless loaded -62 200 61 run return run function rlk:room/raiden/bg/wait
execute in minecraft:overworld unless loaded 61 200 61 run return run function rlk:room/raiden/bg/wait
scoreboard players set #rdBgW rd 0
execute if score #rdBgI rd matches 0 in minecraft:overworld run function rlk:room/raiden/bg/s/0
execute if score #rdBgI rd matches 1 in minecraft:overworld run function rlk:room/raiden/bg/s/1
execute if score #rdBgI rd matches 2 in minecraft:overworld run function rlk:room/raiden/bg/s/2
execute if score #rdBgI rd matches 3 in minecraft:overworld run function rlk:room/raiden/bg/s/3
execute if score #rdBgI rd matches 4 in minecraft:overworld run function rlk:room/raiden/bg/s/4
execute if score #rdBgI rd matches 5 in minecraft:overworld run function rlk:room/raiden/bg/s/5
execute if score #rdBgI rd matches 6 in minecraft:overworld run function rlk:room/raiden/bg/s/6
execute if score #rdBgI rd matches 7 in minecraft:overworld run function rlk:room/raiden/bg/s/7
execute if score #rdBgI rd matches 8 in minecraft:overworld run function rlk:room/raiden/bg/s/8
execute if score #rdBgI rd matches 9 in minecraft:overworld run function rlk:room/raiden/bg/s/9
execute if score #rdBgI rd matches 10 in minecraft:overworld run function rlk:room/raiden/bg/s/10
execute if score #rdBgI rd matches 11 in minecraft:overworld run function rlk:room/raiden/bg/s/11
execute if score #rdBgI rd matches 12 in minecraft:overworld run function rlk:room/raiden/bg/s/12
execute if score #rdBgI rd matches 13 in minecraft:overworld run function rlk:room/raiden/bg/s/13
execute if score #rdBgI rd matches 14 in minecraft:overworld run function rlk:room/raiden/bg/s/14
execute if score #rdBgI rd matches 15 in minecraft:overworld run function rlk:room/raiden/bg/s/15
execute if score #rdBgI rd matches 16 in minecraft:overworld run function rlk:room/raiden/bg/s/16
execute if score #rdBgI rd matches 17 in minecraft:overworld run function rlk:room/raiden/bg/s/17
execute if score #rdBgI rd matches 18 in minecraft:overworld run function rlk:room/raiden/bg/s/18
execute if score #rdBgI rd matches 19 in minecraft:overworld run function rlk:room/raiden/bg/s/19
scoreboard players add #rdBgI rd 1
execute if score #rdBgI rd matches 1..19 run schedule function rlk:room/raiden/bg/tick 1t replace
