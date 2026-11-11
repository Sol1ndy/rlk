# The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat tip; H at its end; locked from tick 0 into the coda.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/seq/ending/m/stage
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/ending/m/lie
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/rig/follow_now
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^3.2 ^1.3 ^2.6
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.1 ^3
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam1,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-1.3 ^1.5 ^2.2
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.5 ^2.1
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] run function rlk:boss/scarlet/seq/lib/camin
execute as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] unless entity @e[type=minecraft:marker,tag=rlk_cine_root,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
function rlk:char/cine/play {clip:"ending"}
function rlk:boss/scarlet/rig/play/ending
scoreboard players set #sqdone hr 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/ending/lock
function rlk:boss/scarlet/fx/hud/ovl {g:"white",in:0,hold:2,out:1}
