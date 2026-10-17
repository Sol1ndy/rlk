# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden).
function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/chaos/reset
scoreboard players set #gdSt mb 7
scoreboard players set #gdRecOn mb 0
scoreboard players set #gdBq1 mb 0
scoreboard players set #gdBq2 mb 0
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/rig/eye/geo
function rlk:mboss/guardian/rig/play/death
function rlk:mboss/guardian/voice/death
playsound minecraft:entity.wither.ambient hostile @a[tag=player] ~ ~ ~ 0.25 1.6 0.3
