# @s = body: stop whatever runs (hazards, props, pull, movement, slot pattern, guard, chaos, a hop back).
function rlk:mboss/lib_clear
kill @e[type=minecraft:marker,tag=rlk_mb_gd_bk]
function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/chaos/reset
scoreboard players set #gdRecOn mb 0
scoreboard players set #gdRecNew mb 0
scoreboard players set #gdBq1 mb 0
scoreboard players set #gdBq2 mb 0
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/rig/eye/geo
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/rig/play/idle
scoreboard players set #gdCool mb 10
function rlk:mboss/guardian/ai/enter
