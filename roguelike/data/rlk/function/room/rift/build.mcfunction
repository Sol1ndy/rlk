# @s = the new anchor (the rlk_riftc marker), at it, rotated toward the zone centre; #riftSt room = 1 dormant / 2
# open; #riftZid room = its zone. The anchor becomes rlk_rift; the parts (rlk_rift_part, zid) are summoned dormant
# and an open rift is opened at once (open_now: full size, the hover object) without the grow animation.
tag @s remove rlk_riftc
tag @s add rlk_rift
scoreboard players operation @s zid = #riftZid room
scoreboard players operation @s riftS = #riftSt room
scoreboard players set @s riftT 0
scoreboard players set @s riftCd 0
scoreboard players set @s riftDw 0
scoreboard players set @s riftPk 0
execute store result score @s riftX run data get entity @s Pos[0] 100
execute store result score @s riftY run data get entity @s Pos[1] 100
execute store result score @s riftZ run data get entity @s Pos[2] 100
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_void","rlk_rift_new"],billboard:"vertical",brightness:{sky:0,block:0},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/void"}},transformation:{translation:[0f,0.8f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.3f,1.3f,1.3f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_rim","rlk_rift_new"],billboard:"vertical",brightness:{sky:6,block:6},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/rim"}},transformation:{translation:[0f,0.8f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.508f,1.508f,1.508f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_crack","rlk_rift_new"],billboard:"fixed",brightness:{sky:10,block:10},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/crack"}},transformation:{translation:[0f,0.02f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f],right_rotation:[0f,0f,0f,1f]},Rotation:[0f,0f]}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_arc0","rlk_rift_new"],billboard:"center",brightness:{sky:15,block:15},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/arc_0"}},transformation:{translation:[-0.4f,1.025f,0.05f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_arc1","rlk_rift_new"],billboard:"center",brightness:{sky:15,block:15},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/arc_1"}},transformation:{translation:[0f,1.45f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_rift_part","rlk_rift_arc2","rlk_rift_new"],billboard:"center",brightness:{sky:15,block:15},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:rift/arc_2"}},transformation:{translation:[0f,1.45f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_rift_new,tag=rlk_rift_crack] at @s run tp @s ~ ~ ~ ~ 0
scoreboard players operation @e[tag=rlk_rift_new] zid = #riftZid room
scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc0] riftA 0
scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc1] riftA 1
scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc2] riftA 2
tag @e[tag=rlk_rift_arc0,tag=rlk_rift_new] add rlk_rift_arc
tag @e[tag=rlk_rift_arc1,tag=rlk_rift_new] add rlk_rift_arc
tag @e[tag=rlk_rift_arc2,tag=rlk_rift_new] add rlk_rift_arc
tag @e[tag=rlk_rift_new] remove rlk_rift_new
execute if score @s riftS matches 2 run function rlk:room/rift/open_now
execute if score @s riftS matches 1 run function rlk:room/rift/snd/dormant
