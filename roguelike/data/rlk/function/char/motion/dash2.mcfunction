# @s = player (char/motion/dash): the double dodge's second move, an aerial cartwheel along the dodge direction (9 ticks;
# rig characters: clip dash2, mannequin characters: the stand-in rig, lite/f).
execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"dash2"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"dash2"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"dash2"}
execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX
execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ
execute if data storage rlk:player_motion active{clip:"dash2"} run return run function rlk:char/motion/dash_face with storage rlk:player_motion face
execute if score #charN tmp matches 1 run function rlk:char/motion/lite/start_f
execute if score #charN tmp matches 4 run function rlk:char/motion/lite/start_f
execute if score #charN tmp matches 7 run function rlk:char/motion/lite/start_f
execute if score #charN tmp matches 8 run function rlk:char/motion/lite/start_f
execute if score @s plActive matches 1 if score @s plClip matches 3 run function rlk:char/motion/lite/face with storage rlk:player_motion face
