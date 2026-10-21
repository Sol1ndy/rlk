# Play aftermath (224 t, clip id 29) from its tick 0 (@s = the body). The
# px sets of the clip follow it (pxs/tick reads the rig clock); the stance / looks / hands are the rig's.
function rlk:mboss/apep/rig/play/aftermath
# the yaw schedule of the manifest turns the anchor (sign #apYawS: -1 mirrors it)
scoreboard players set #apYawC mb 29
scoreboard players operation #apYawSg mb = #apYawS mb
scoreboard players set #apYawS mb 1
scoreboard players set #apYawT mb -1
execute store result score #apYaw0 mb run data get entity @s Rotation[0] 100
