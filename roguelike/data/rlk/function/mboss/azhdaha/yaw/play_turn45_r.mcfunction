# Play turn45_r and arm the yaw driver (the anchor turns by the
# manifest schedule; teleport_duration carries it).
function rlk:mboss/azhdaha/rig/play/turn45_r
scoreboard players set #azYawC mb 4
scoreboard players set #azYawS mb 1
scoreboard players set #azYawT mb -1
execute store result score #azYaw0 mb run data get entity @s Rotation[0] 100
