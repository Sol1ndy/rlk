# @s = zone marker, positioned at this box's floor spot, rotated toward the player. item_display turns item
# models 180 degrees, so yaw = toward the player + 180 puts the chest's latch toward the player; 90 more
# are turned back while falling. Boxes after the first wait 4 ticks each (mbT starts at 0, -4, ...).
summon minecraft:item_display ~ ~6.55 ~ {Tags:["rlk_room","rlk_mb_box","rlk_mb_boxfall","rlk_mb_boxnew"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:chest",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_boxnew] run tp @s ~ ~6.55 ~ ~270 0
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_boxnew] mbT 0
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_boxnew] mbT -= #mbBoxW mb
tag @e[type=minecraft:item_display,tag=rlk_mb_boxnew] remove rlk_mb_boxnew
scoreboard players add #mbBoxW mb 4
