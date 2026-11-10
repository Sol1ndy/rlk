# @s = player, from player/def/guard (a parry press): play the character guard clip when it has one.
execute if score #charN tmp matches 5 run function rlk:char/motion/start {char:"arle",clip:"guard"}
execute if score #charN tmp matches 3 run function rlk:char/motion/start {char:"skirk",clip:"guard"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"guard"}
