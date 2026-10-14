# @s = player, from player/dash_go: play the character dash clip when it has one.
execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"dash"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"dash"}
execute unless data storage rlk:player_motion active{clip:"dash"} run return 0
execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX
execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ
function rlk:char/motion/dash_face with storage rlk:player_motion face
