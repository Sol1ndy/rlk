kill @e[tag=rvpR]
kill @e[tag=rvpH]
kill @e[tag=rvpN]
summon minecraft:armor_stand 4.5 120 0.5 {Tags:["rvpR","rlk_body"],Rotation:[135f,0f],NoGravity:1b}
data modify storage rvp:log a06 set value {}
execute as @e[tag=rvpR] at @s run function rlk:player/def/dodge_stamp
data modify storage rvp:log a06.box_rot set from entity @e[tag=rlk_dgo,limit=1] Rotation
tp @e[tag=rvpR] 7.5 120 0.5 20 0
function rlk:player/def/ghost_on
execute as @e[tag=rvpR] run function rlk:player/def/fx/pd
function rlk:player/def/ghost_off
data modify storage rvp:log a06.ghost_rot set from entity @e[tag=rlk_cb_ghost,limit=1] Rotation
data modify storage rvp:log a06.ghost_pos set from entity @e[tag=rlk_cb_ghost,limit=1] Pos
execute store result storage rvp:log a06.red_team int 1 if entity @e[tag=rlk_cb_ghost,team=rlk_cbred]
execute store result storage rvp:log a06.body_back int 1 if entity @e[tag=rvpR,tag=rlk_body]
data modify storage rvp:log rows2 set value []
scoreboard players set #t rvp 0
scoreboard players set #mode rvp 4
