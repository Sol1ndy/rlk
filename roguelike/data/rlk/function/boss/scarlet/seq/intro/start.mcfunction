# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Start (@s = the body, at it; #sq hr = 0).
kill @e[type=minecraft:marker,tag=rlk_hr_stage]
kill @e[type=minecraft:marker,tag=rlk_hr_stage2]
summon minecraft:marker 881.28 201 25.55 {Tags:["rlk_room","rlk_mb_aux","rlk_hr_stage"]}
execute as @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] at @s facing 884.0 201 5.0 run tp @s ~ ~ ~ ~ 0
# the one avatar teleport: the player (and with them the avatar and the fall marker) to the stage origin, under the
# arrival blindness
execute as @a[tag=player,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @a[tag=player,limit=1] run function rlk:view/sync
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run tp @e[tag=rlk_safe,limit=1] ~ ~ ~
function rlk:mboss/cam/kill
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:mboss/cam/spawn
execute as @a[tag=player,limit=1] unless entity @s[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] run function rlk:char/cine/spawn
function rlk:char/cine/play {clip:"cs0"}
function rlk:boss/scarlet/rig/play/intro
scoreboard players set #sqdone hr 0
scoreboard players set #sq_cx hr 0
scoreboard players set #sq_h hr 0
scoreboard players set @a[tag=player] hudHold 2
title @a[tag=player] actionbar ""
execute unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/intro/lock
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^0 ^-7.5 run function rlk:boss/scarlet/fx/p/arrive_rift
function rlk:boss/scarlet/fx/p/ambient_p1
execute at @a[tag=player,limit=1] run function rlk:boss/scarlet/fx/snd/cs0_wind
