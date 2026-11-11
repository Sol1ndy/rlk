# repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.
# Start (@s = the body, at it; #sq hr = 0) — macro.
$scoreboard players set #sq_at hr $(at)
scoreboard players set #sq_keep hr 0
function rlk:boss/scarlet/seq/repel/m/stage
scoreboard players set #mbNoLeash mb 1
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/repel/m/drop
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
function rlk:boss/scarlet/seq/repel/m/land
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^1.2 ^0.9 ^0.65
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.55 ^0.65
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/lift
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.55 ^0.65
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:1}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] ^-2.2 ^1.5 ^0.1
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/ar/clampw
execute as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:boss/scarlet/seq/lib/over
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] facing ^0 ^1.4 ^0.8
execute at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run function rlk:mboss/cam/spawn_at {id:2}
kill @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1]
execute as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
function rlk:char/cine/play {clip:"repel"}
function rlk:boss/scarlet/rig/play/repel
scoreboard players set #sqdone hr 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/repel/lock
function rlk:boss/scarlet/fx/hud/ovl {g:"gold",in:0,hold:4,out:3}
function rlk:boss/scarlet/fx/snd/deflect
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.55 ^0.65 run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^1.55 ^0.65 run function rlk:boss/scarlet/fx/p/light_column
