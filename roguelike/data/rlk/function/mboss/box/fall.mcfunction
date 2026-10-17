# @s = falling box, at @s. mbT <= 0: waiting for its turn up in the air (sparkles).
execute if score @s mbT matches ..0 run return run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.01 1
execute if score @s mbT matches 1 run tp @s ~ ~-0.1301 ~ ~-12.398 ~
execute if score @s mbT matches 2 run tp @s ~ ~-0.176 ~ ~-11.4796 ~
execute if score @s mbT matches 3 run tp @s ~ ~-0.2219 ~ ~-10.5612 ~
execute if score @s mbT matches 4 run tp @s ~ ~-0.2679 ~ ~-9.6429 ~
execute if score @s mbT matches 5 run tp @s ~ ~-0.3138 ~ ~-8.7245 ~
execute if score @s mbT matches 6 run tp @s ~ ~-0.3597 ~ ~-7.8061 ~
execute if score @s mbT matches 7 run tp @s ~ ~-0.4056 ~ ~-6.8878 ~
execute if score @s mbT matches 8 run tp @s ~ ~-0.4515 ~ ~-5.9694 ~
execute if score @s mbT matches 9 run tp @s ~ ~-0.4974 ~ ~-5.051 ~
execute if score @s mbT matches 10 run tp @s ~ ~-0.5434 ~ ~-4.1327 ~
execute if score @s mbT matches 11 run tp @s ~ ~-0.5893 ~ ~-3.2143 ~
execute if score @s mbT matches 12 run tp @s ~ ~-0.6352 ~ ~-2.2959 ~
execute if score @s mbT matches 13 run tp @s ~ ~-0.6811 ~ ~-1.3776 ~
execute if score @s mbT matches 14 run tp @s ~ ~-0.7271 ~ ~-0.459 ~
execute if score @s mbT matches 1..13 at @s run function rlk:mboss/box/trail
execute if score @s mbT matches 14 at @s run function rlk:mboss/box/land
execute if score @s mbT matches 17 run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,0f,0f],scale:[1.1f,1.1f,1.1f]}}
execute if score @s mbT matches 20.. run function rlk:mboss/box/settle
