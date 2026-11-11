# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/seq/cs1/m/stage
scoreboard players set #mbNoLeash mb 1
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/cs1/m/mark
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^9 ^2.2 ^4.5
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.2 ^4.5
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^2.6 ^1.3 ^0.8
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.45 ^0.75
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
function rlk:char/cine/play {clip:"cs1"}
function rlk:boss/scarlet/rig/play/cs1
scoreboard players set #sqdone hr 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set #sq_sk hr 0
scoreboard players set #sq_sks hr -1
scoreboard players set #sq_skd hr 0
scoreboard players set #sq_skn hr 0
scoreboard players set #skip hr -1
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
function rlk:boss/scarlet/fx/hud/ovl {g:"white",in:0,hold:2,out:2}
