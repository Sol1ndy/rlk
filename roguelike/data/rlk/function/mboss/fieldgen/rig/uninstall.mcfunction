# Removes the rig, its props and its objectives.
function rlk:mboss/fieldgen/rig/kill
function rlk:mboss/fieldgen/rig/prop/clear
kill @e[type=marker,tag=rlk_mb_fg_face]
scoreboard objectives remove fgRigC
scoreboard objectives remove fgRigT
scoreboard objectives remove fgRigF
scoreboard objectives remove fgRigY
scoreboard objectives remove fgRigForm
scoreboard objectives remove fgRigLook
scoreboard objectives remove fgRigCrack
scoreboard objectives remove fgRigTmp
