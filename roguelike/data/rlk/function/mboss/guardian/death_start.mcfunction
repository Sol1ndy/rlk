# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden).
function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/chaos/reset
scoreboard players set #gdSt mb 7
scoreboard players set #gdRecOn mb 0
scoreboard players set #gdBq1 mb 0
scoreboard players set #gdBq2 mb 0
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/rig/eye/geo
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/rig/play/death
function rlk:mboss/guardian/voice/death
# no creature vocals (K18): the typed line, a soft crystal sting and the framework's non-vocal death sound
playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
