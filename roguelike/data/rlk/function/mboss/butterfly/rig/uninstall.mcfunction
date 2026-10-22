# Removes the rig, its props and its objectives.
function rlk:mboss/butterfly/rig/kill
function rlk:mboss/butterfly/rig/prop/clear
kill @e[type=marker,tag=rlk_mb_bf_face]
scoreboard objectives remove bfRigC
scoreboard objectives remove bfRigT
scoreboard objectives remove bfRigF
scoreboard objectives remove bfRigY
scoreboard objectives remove bfRigForm
scoreboard objectives remove bfRigLook
scoreboard objectives remove bfRigFlat
scoreboard objectives remove bfRigTell
