# @s = the body of cproto (anchor), at it: its 2 hit proxies (interactions, UUID block 524c4b4d-4350-4400-8000-0000000000.., low byte
# pxBase 65 + k) summoned parked, then the current state set (px.set; inv at a fight start) applied. A /reload
# respawns them from rlk:mboss px (the offsets and tops of the last pose written).
kill 524c4b4d-4350-4400-8000-000000000041
kill 524c4b4d-4350-4400-8000-000000000042
execute unless data storage rlk:mboss px.o run data modify storage rlk:mboss px.o set value {core_x:0d,core_y:-8d,core_z:0d,tail_x:0d,tail_y:-8d,tail_z:-2.4d}
execute unless data storage rlk:mboss px.top run data modify storage rlk:mboss px.top set value {core:2.4f,tail:1.2f}
execute unless data storage rlk:mboss px.set run data modify storage rlk:mboss px.set set value "inv"
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1129333760,-2147483648,65],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_core"],width:2f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4350-4400-8000-000000000041 mbPart 1
execute store result score #t mb run data get storage rlk:mboss px.top.core 100
scoreboard players set #pxU1 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU1 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4350-4400-8000-000000000041 height float 0.01 run scoreboard players get #t mb
execute at @s rotated as @s rotated ~ 0 positioned ^ ^-8 ^ run summon minecraft:interaction ~ ~ ~ {UUID:[I;1380731725,1129333760,-2147483648,66],Tags:["rlk_room","rlk_mb_aux","boss","rlk_mb_px","rlk_mb_px_tail"],width:1.2f,height:1.0f,response:false}
scoreboard players set 524c4b4d-4350-4400-8000-000000000042 mbPart 2
execute store result score #t mb run data get storage rlk:mboss px.top.tail 100
scoreboard players set #pxU2 mb 0
execute if score #t mb matches 31.. run scoreboard players set #pxU2 mb 1
execute if score #t mb matches ..10 run scoreboard players set #t mb 10
execute store result entity 524c4b4d-4350-4400-8000-000000000042 height float 0.01 run scoreboard players get #t mb
function rlk:mboss/px/state with storage rlk:mboss px
