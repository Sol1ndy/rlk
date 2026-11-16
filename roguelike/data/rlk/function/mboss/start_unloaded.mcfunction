# @s = zone marker. The arena chunks are not loaded (their forceload was released, e.g. room/remove then
# room/setup without a /reload): forceload them again and retry every 10 ticks; the 7th miss in a row (3 s) cancels
# the fight without reward like a failed spawn (the gate comes back).
execute in minecraft:overworld run function rlk:mboss/ar/fl_on
scoreboard players add #mbLd mb 1
execute if score #mbLd mb matches ..6 run return run scoreboard players set #spawnT room 10
function rlk:mboss/start_cancel
