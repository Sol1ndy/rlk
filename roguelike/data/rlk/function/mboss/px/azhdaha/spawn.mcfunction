# @s = the body of azhdaha (anchor), at it: its 12 hit proxies (interactions, UUID block 524c4b4d-415a-4400-8000-0000000000.., low byte
# pxBase 65 + k) summoned parked, then the current state set (px.set; inv at a fight start) applied. A /reload
# respawns them from rlk:mboss px (the offsets and tops of the last pose written).
kill 524c4b4d-415a-4400-8000-000000000041
kill 524c4b4d-415a-4400-8000-000000000042
kill 524c4b4d-415a-4400-8000-000000000043
kill 524c4b4d-415a-4400-8000-000000000044
kill 524c4b4d-415a-4400-8000-000000000045
kill 524c4b4d-415a-4400-8000-000000000046
kill 524c4b4d-415a-4400-8000-000000000047
kill 524c4b4d-415a-4400-8000-000000000048
kill 524c4b4d-415a-4400-8000-000000000049
kill 524c4b4d-415a-4400-8000-00000000004a
kill 524c4b4d-415a-4400-8000-00000000004b
kill 524c4b4d-415a-4400-8000-00000000004c
execute unless data storage rlk:mboss px.o run data modify storage rlk:mboss px.o set value {head_x:0d,head_y:-8d,head_z:4.3d,chest_x:0d,chest_y:-8d,chest_z:2.1d,belly_x:0d,belly_y:-8d,belly_z:-0.5d,hips_x:0d,hips_y:-8d,hips_z:-3.4d,tail1_x:0d,tail1_y:-8d,tail1_z:-6.35d,tail2_x:0d,tail2_y:-8d,tail2_z:-10.12d,tail3_x:0d,tail3_y:-8d,tail3_z:-12.86d,tail4_x:0d,tail4_y:-8d,tail4_z:-11.9d,paw_l_x:3.15d,paw_l_y:-8d,paw_l_z:2.95d,paw_r_x:-3.15d,paw_r_y:-8d,paw_r_z:2.95d,foot_l_x:2.5d,foot_l_y:-8d,foot_l_z:-2.55d,foot_r_x:-2.5d,foot_r_y:-8d,foot_r_z:-2.55d}
execute unless data storage rlk:mboss px.top run data modify storage rlk:mboss px.top set value {head:3.05f,chest:4.85f,belly:4.85f,hips:4.2f,tail1:3.94f,tail2:3.9f,tail3:5.81f,tail4:8.51f,paw_l:2.8f,paw_r:2.8f,foot_l:2.92f,foot_r:2.92f}
execute unless data storage rlk:mboss px.set run data modify storage rlk:mboss px.set set value "inv"
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,65],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_head"],width:2.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000041 mbPart 1
execute store result score #t mb run data get storage rlk:mboss px.top.head 100
scoreboard players set #pxU1 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU1 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000041 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,66],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_chest"],width:4.6f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000042 mbPart 2
execute store result score #t mb run data get storage rlk:mboss px.top.chest 100
scoreboard players set #pxU2 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU2 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000042 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,67],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_belly"],width:4.6f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000043 mbPart 3
execute store result score #t mb run data get storage rlk:mboss px.top.belly 100
scoreboard players set #pxU3 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU3 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000043 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,68],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_hips"],width:4.4f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000044 mbPart 4
execute store result score #t mb run data get storage rlk:mboss px.top.hips 100
scoreboard players set #pxU4 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU4 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000044 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,69],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail1"],width:2.6f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000045 mbPart 5
execute store result score #t mb run data get storage rlk:mboss px.top.tail1 100
scoreboard players set #pxU5 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU5 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000045 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,70],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail2"],width:2.2f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000046 mbPart 6
execute store result score #t mb run data get storage rlk:mboss px.top.tail2 100
scoreboard players set #pxU6 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU6 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000046 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,71],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail3"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000047 mbPart 7
execute store result score #t mb run data get storage rlk:mboss px.top.tail3 100
scoreboard players set #pxU7 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU7 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000047 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,72],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail4"],width:1.4f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000048 mbPart 8
execute store result score #t mb run data get storage rlk:mboss px.top.tail4 100
scoreboard players set #pxU8 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU8 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000048 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,73],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_paw_l"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-000000000049 mbPart 9
execute store result score #t mb run data get storage rlk:mboss px.top.paw_l 100
scoreboard players set #pxU9 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU9 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-000000000049 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,74],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_paw_r"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-00000000004a mbPart 10
execute store result score #t mb run data get storage rlk:mboss px.top.paw_r 100
scoreboard players set #pxU10 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU10 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-00000000004a height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,75],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_foot_l"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-00000000004b mbPart 11
execute store result score #t mb run data get storage rlk:mboss px.top.foot_l 100
scoreboard players set #pxU11 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU11 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-00000000004b height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1096434688,-2147483648,76],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_foot_r"],width:1.8f,height:1.0f,response:false}
scoreboard players set 524c4b4d-415a-4400-8000-00000000004c mbPart 12
execute store result score #t mb run data get storage rlk:mboss px.top.foot_r 100
scoreboard players set #pxU12 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU12 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-415a-4400-8000-00000000004c height float 0.01 run scoreboard players get #t mb
function rlk:mboss/px/state with storage rlk:mboss px
