# @s = an arc card: frame (#riftF + riftA) mod 4; every second call a new roll angle. Dormant: arcs 1 and 2 rest.
execute if score #riftSt room matches 1 unless score @s riftA matches 0 run return 0
scoreboard players operation #riftAf room = #riftF room
scoreboard players operation #riftAf room += @s riftA
scoreboard players operation #riftAf room %= #riftC4 room
execute if score #riftAf room matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:rift/arc_0"
execute if score #riftAf room matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:rift/arc_1"
execute if score #riftAf room matches 2 run data modify entity @s item.components."minecraft:item_model" set value "rlk:rift/arc_2"
execute if score #riftAf room matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:rift/arc_3"
execute if score #riftRl room matches 1 run return 0
execute store result score #riftAr room run random value 0..7
execute if score #riftAr room matches 0 run data merge entity @s {transformation:{left_rotation:{angle:-0.9f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 1 run data merge entity @s {transformation:{left_rotation:{angle:-0.55f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 2 run data merge entity @s {transformation:{left_rotation:{angle:-0.25f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 3 run data merge entity @s {transformation:{left_rotation:{angle:0f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 4 run data merge entity @s {transformation:{left_rotation:{angle:0.3f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 5 run data merge entity @s {transformation:{left_rotation:{angle:0.6f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 6 run data merge entity @s {transformation:{left_rotation:{angle:0.95f,axis:[0f,0f,1f]}}}
execute if score #riftAr room matches 7 run data merge entity @s {transformation:{left_rotation:{angle:3.14f,axis:[0f,0f,1f]}}}
