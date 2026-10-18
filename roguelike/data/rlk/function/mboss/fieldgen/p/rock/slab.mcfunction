scoreboard players add @s mbT 1
execute if score @s mbT matches 0 run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[0f,0f,0f],left_rotation:[0.08f,0.2f,0f,0.976f],right_rotation:[0f,0f,0f,1f],scale:[2.2f,0.9f,0.6f]}}
execute if score @s mbT matches 0 run tp @s ~ ~4 ~
execute if score @s mbT matches 0 run particle minecraft:block{block_state:"minecraft:tuff"} ~ ~ ~ 0.6 0.2 0.6 0 12 force @a[tag=player]
scoreboard players operation #fgM mb = @s mbT
scoreboard players operation #fgM mb %= #fgK4 mb
execute if score @s mbT matches 1.. if score #fgM mb matches 0 run particle minecraft:falling_dust{block_state:"minecraft:tuff"} ~ ~-0.3 ~ 0.5 0.1 0.5 0 1 force @a[tag=player]
