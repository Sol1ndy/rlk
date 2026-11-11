# @s = player (player/dodge/away: the dodge avoided an attack; not over the perfect dodge's handspring or the cartwheel):
# the upright back-step (clip dash_b, 8 ticks) facing the attacker - the basis is turned against the move (dashUX / dashUZ x -1).
execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"dash_b"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"dash_b"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"dash_b"}
execute if score #charN tmp matches 1 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 4 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 7 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute if score #charN tmp matches 8 if entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] run function rlk:player/dodge/crouch
execute unless data storage rlk:player_motion active{clip:"dash_b"} run return 0
execute store result storage rlk:player_motion face.dx double -0.01 run scoreboard players get @s dashUX
execute store result storage rlk:player_motion face.dz double -0.01 run scoreboard players get @s dashUZ
function rlk:char/motion/dash_face with storage rlk:player_motion face
