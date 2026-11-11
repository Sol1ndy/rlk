# The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat tip; H at its end; locked from tick 0 into the coda.
# Start (@s = the body, at it; #sq hr = 0).
function rlk:boss/scarlet/seq/ending/m/stage
function rlk:mboss/mv/stop
function rlk:boss/scarlet/seq/ending/m/lie
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run rotate @s ~180 0
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:mboss/cam/spawn
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
