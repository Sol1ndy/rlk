# @s = player, from player/dash_go: play the character dash clip when it has one.
execute unless data storage rlk:player_motion active{clip:"dash"} run return 0
execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX
execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ
function rlk:char/motion/dash_face with storage rlk:player_motion face
