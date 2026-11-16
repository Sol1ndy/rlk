# @s = body: every slot and its lingering effects cut, the idle pose shown once (then held).
function rlk:mboss/lib_clear
function rlk:boss/azhdaha/p/cancel
function rlk:boss/azhdaha/cast/cancel
function rlk:boss/azhdaha/bg/cancel_l
function rlk:boss/azhdaha/bg/cancel_t
function rlk:boss/azhdaha/fld/clear
kill @e[tag=rlk_mb_az_orb]
kill @e[tag=rlk_mb_az_orbc]
function rlk:boss/azhdaha/aft/clear
function rlk:boss/azhdaha/fx/tele/clear
function rlk:boss/azhdaha/rig/glow/gold_off
scoreboard players set #azOrbHigh mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #azYawC mb 0
function rlk:boss/azhdaha/rig/play/idle
function rlk:boss/azhdaha/rig/tick
scoreboard players set #azHudQ mb 1
