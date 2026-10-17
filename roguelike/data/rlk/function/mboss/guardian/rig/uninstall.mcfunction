# Removes the rig, its props and its objectives.
function rlk:mboss/guardian/rig/kill
function rlk:mboss/guardian/rig/prop/clear
kill @e[type=marker,tag=rlk_mb_gd_face]
scoreboard objectives remove gdRigC
scoreboard objectives remove gdRigT
scoreboard objectives remove gdRigF
scoreboard objectives remove gdRigEye
scoreboard objectives remove gdRigSp
scoreboard objectives remove gdRigY
