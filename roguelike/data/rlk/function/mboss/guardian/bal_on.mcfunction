# @s = body: cut the slot pattern and the library effects (the guard / chaos counters stay), kneel.
function rlk:mboss/lib_clear
kill @e[type=minecraft:marker,tag=rlk_mb_gd_bk]
function rlk:mboss/guardian/p/cancel
function rlk:mboss/guardian/rig/spear/geo
function rlk:mboss/guardian/rig/eye/geo
function rlk:mboss/guardian/rig/glow/off
function rlk:mboss/guardian/rig/play/groggy_a
scoreboard players set #gdT mb 0
scoreboard players set #mbNoLeash mb 0
playsound minecraft:block.amethyst_block.fall hostile @a[tag=player] ~ ~ ~ 0.9 0.8 0.3
function rlk:mboss/guardian/hud/sub_groggy
