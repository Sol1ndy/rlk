# @s = player. Into the arena: short blindness hides the jump; avatar and fall marker follow.
effect give @s minecraft:blindness 1 0 true
function rlk:mboss/tp_start with storage rlk:mboss cur.start
function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
execute at @s run playsound minecraft:entity.enderman.teleport hostile @s ~ ~ ~ 0.6 0.6
execute at @s run playsound minecraft:block.beacon.activate hostile @s ~ ~ ~ 0.6 0.7
