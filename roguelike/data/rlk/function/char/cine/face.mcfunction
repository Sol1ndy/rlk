# function rlk:char/cine/face {yaw:<degrees>}: turns the root to that absolute yaw over 12 ticks (the ending's ST -> ST2).
# The clip's own root yaw is inside the pose and adds to it.
scoreboard objectives add cine dummy
$data modify storage rlk:cine face set value {yaw:$(yaw)}
execute store result score #cavFy cine run data get storage rlk:cine face.yaw 100
scoreboard players set #cavF cine 12
