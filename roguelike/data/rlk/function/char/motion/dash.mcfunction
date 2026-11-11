# @s = player, from player/dash_go: the avatar's dodge motion (round W: the reference game's dodge set; build_player_beat.mjs).
# #dgMv cb 1 = the plain dodge: a quick crouching hop-step (rig characters: clip dash, 6 ticks; mannequin characters: the
# mannequin's own crouch pose until player/dodge/stand), 2 = the second move of a double dodge (char/motion/dash2).
# The clip's yaw is locked and its basis turned to the dodge direction (player/dash_dir: dashUX / dashUZ, unit x 100).
execute if score #dgMv cb matches 2 run return run function rlk:char/motion/dash2
execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"dash"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"dash"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"dash"}
execute if score #charN tmp matches 1 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 4 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 7 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 8 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute unless data storage rlk:player_motion active{clip:"dash"} run return 0
execute store result storage rlk:player_motion face.dx double 0.01 run scoreboard players get @s dashUX
execute store result storage rlk:player_motion face.dz double 0.01 run scoreboard players get @s dashUZ
function rlk:char/motion/dash_face with storage rlk:player_motion face
