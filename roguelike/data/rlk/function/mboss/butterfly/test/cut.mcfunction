# @s = body: stop whatever runs (hazards, props, pull, movement, slot pattern, close-in, look prep, groggy).
function rlk:mboss/lib_clear
function rlk:mboss/butterfly/p/cancel
function rlk:mboss/butterfly/rig/prop/clear
scoreboard players set #bfMv mb 0
execute if score #bfForm mb matches 1 run function rlk:mboss/butterfly/rig/play/idle_h
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/rig/play/idle_b
scoreboard players set #bfCool mb 10
function rlk:mboss/butterfly/ai/enter
