# Removes the rig and its objectives.
function rlk:mboss/azhdaha/rig/kill
kill @e[type=marker,tag=rlk_mb_az_face]
scoreboard objectives remove azRigC
scoreboard objectives remove azRigT
scoreboard objectives remove azRigF
scoreboard objectives remove azRigY
scoreboard objectives remove azRigLegs
scoreboard objectives remove azRigTail
scoreboard objectives remove azRigState
