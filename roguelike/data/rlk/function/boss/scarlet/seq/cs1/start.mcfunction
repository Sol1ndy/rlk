# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/seq/cs1/m/stage
scoreboard players set #mbNoLeash mb 1
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/cs1/m/mark
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:mboss/cam/spawn
execute as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
function rlk:char/cine/play {clip:"cs1"}
function rlk:boss/scarlet/rig/play/cs1
scoreboard players set #sqdone hr 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
function rlk:boss/scarlet/fx/hud/ovl {g:"white",in:0,hold:2,out:2}
