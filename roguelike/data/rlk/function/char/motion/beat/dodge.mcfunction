# @s = player, 5 ticks after the dodged hit (player/def/beat/d/clock): upright with both arms raised, arching back through the
# slow motion, then the back handspring and the landing facing the attacker (clip pdodge; ref_pd.md 4).
# Not when the player has acted since the dodge (an attack, a skill, another dodge or F: player/def/beat/act; a rig character: a
# clip other than the dash is playing): the flip is presentation and never cuts the player's own action.
execute if score #btAct cb matches 1 run return 0
execute if score @s pmMoveLock matches 1 run return 0
execute if score @s pmActive matches 1 unless data storage rlk:player_motion active{clip:"dash"} run return 0
execute if score #charN tmp matches 5 unless score @s arM matches 1.. run function rlk:char/motion/start {char:"arle",clip:"pdodge"}
execute if score #charN tmp matches 5 if score @s arM matches 1.. run function rlk:char/motion/start {char:"arle",clip:"pdodge_i"}
execute if score #charN tmp matches 3 unless score @s skM matches 1.. run function rlk:char/motion/start {char:"skirk",clip:"pdodge"}
execute if score #charN tmp matches 3 if score @s skM matches 1.. run function rlk:char/motion/start {char:"skirk",clip:"pdodge_i"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"pdodge"}
execute if data storage rlk:player_motion active{clip:"pdodge"} run function rlk:char/motion/beat/face
execute if data storage rlk:player_motion active{clip:"pdodge_i"} run function rlk:char/motion/beat/face
execute if score #charN tmp matches 1 run function rlk:char/motion/lite/start_d
execute if score #charN tmp matches 4 run function rlk:char/motion/lite/start_d
execute if score #charN tmp matches 7 run function rlk:char/motion/lite/start_d
execute if score #charN tmp matches 8 run function rlk:char/motion/lite/start_d
function rlk:char/motion/beat/tint_on
