# @s = the body of apep (anchor), at it: its 11 hit proxies (interactions, UUID block 524c4b4d-4150-4400-8000-0000000000.., low byte
# pxBase 65 + k) summoned parked, then the current state set (px.set; inv at a fight start) applied. A /reload
# respawns them from rlk:mboss px (the offsets and tops of the last pose written).
kill 524c4b4d-4150-4400-8000-000000000041
kill 524c4b4d-4150-4400-8000-000000000042
kill 524c4b4d-4150-4400-8000-000000000043
kill 524c4b4d-4150-4400-8000-000000000044
kill 524c4b4d-4150-4400-8000-000000000045
kill 524c4b4d-4150-4400-8000-000000000046
kill 524c4b4d-4150-4400-8000-000000000047
kill 524c4b4d-4150-4400-8000-000000000048
kill 524c4b4d-4150-4400-8000-000000000049
kill 524c4b4d-4150-4400-8000-00000000004a
kill 524c4b4d-4150-4400-8000-00000000004b
execute unless data storage rlk:mboss px.o run data modify storage rlk:mboss px.o set value {head_x:0d,head_y:-8d,head_z:3.4d,chest_x:0d,chest_y:-8d,chest_z:0d,abd_x:0d,abd_y:-8d,abd_z:-2d,tail_a_x:0.2d,tail_a_y:-8d,tail_a_z:-6d,tail_b_x:1.3d,tail_b_y:-8d,tail_b_z:-9.3d,a_l_x:5.3d,a_l_y:-8d,a_l_z:2.6d,a_r_x:-5.3d,a_r_y:-8d,a_r_z:2.6d,b_l_x:2.5d,b_l_y:-8d,b_l_z:3.6d,b_r_x:-2.5d,b_r_y:-8d,b_r_z:3.6d,c_l_x:3d,c_l_y:-8d,c_l_z:-3d,c_r_x:-3d,c_r_y:-8d,c_r_z:-3d}
execute unless data storage rlk:mboss px.top run data modify storage rlk:mboss px.top set value {head:4.5f,chest:5f,abd:4f,tail_a:2f,tail_b:2f,a_l:2.5f,a_r:2.5f,b_l:3f,b_r:3f,c_l:3f,c_r:3f}
execute unless data storage rlk:mboss px.set run data modify storage rlk:mboss px.set set value "inv"
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,65],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_head"],width:2.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000041 mbPart 1
execute store result score #t mb run data get storage rlk:mboss px.top.head 100
scoreboard players set #pxU1 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU1 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000041 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,66],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_chest"],width:3f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000042 mbPart 2
execute store result score #t mb run data get storage rlk:mboss px.top.chest 100
scoreboard players set #pxU2 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU2 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000042 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,67],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_abd"],width:2.6f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000043 mbPart 3
execute store result score #t mb run data get storage rlk:mboss px.top.abd 100
scoreboard players set #pxU3 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU3 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000043 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,68],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail_a"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000044 mbPart 4
execute store result score #t mb run data get storage rlk:mboss px.top.tail_a 100
scoreboard players set #pxU4 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU4 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000044 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,69],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail_b"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000045 mbPart 5
execute store result score #t mb run data get storage rlk:mboss px.top.tail_b 100
scoreboard players set #pxU5 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU5 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000045 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,70],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_a_l"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000046 mbPart 6
execute store result score #t mb run data get storage rlk:mboss px.top.a_l 100
scoreboard players set #pxU6 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU6 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000046 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,71],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_a_r"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000047 mbPart 7
execute store result score #t mb run data get storage rlk:mboss px.top.a_r 100
scoreboard players set #pxU7 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU7 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000047 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,72],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_b_l"],width:2.2f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000048 mbPart 8
execute store result score #t mb run data get storage rlk:mboss px.top.b_l 100
scoreboard players set #pxU8 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU8 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000048 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,73],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_b_r"],width:2.2f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-000000000049 mbPart 9
execute store result score #t mb run data get storage rlk:mboss px.top.b_r 100
scoreboard players set #pxU9 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU9 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-000000000049 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,74],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_c_l"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-00000000004a mbPart 10
execute store result score #t mb run data get storage rlk:mboss px.top.c_l 100
scoreboard players set #pxU10 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU10 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-00000000004a height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1095779328,-2147483648,75],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_c_r"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4150-4400-8000-00000000004b mbPart 11
execute store result score #t mb run data get storage rlk:mboss px.top.c_r 100
scoreboard players set #pxU11 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU11 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4150-4400-8000-00000000004b height float 0.01 run scoreboard players get #t mb
function rlk:mboss/px/state with storage rlk:mboss px
