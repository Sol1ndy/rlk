# Phase 0 -> 1 (rage full while no pattern runs, or a test). Clears every pattern entity and visual, cancels a
# blink, then transform_tick plays the 60 t transformation (immune: combat/apply returns in phase 1).
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdBlink 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/hazard/clear
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
scoreboard players set @s rdPhase 1
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players add @s rdCycle 1
scoreboard players set @s rdAnim 0
scoreboard players operation @s rdRigL = @s rdAnim
tag @s remove rlk_rd_tm_rear
scoreboard players set @s rdTmChain 0
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/line/eternal
scoreboard players set #rdCapPat rd 0
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.3
