# @s = player, on the trigger tick of a perfect dodge (player/def/beat/start_d; round W: at once, no wind-up): the back
# handspring - launch, 360 degrees backward in 6 ticks, landed facing the attacker on tick 7, the ready stance on tick 10 (clip
# pdodge) - and the red-pink body glow. Rig characters play their clip, mannequin characters the stand-in rig.
# Not while a move-locked action plays, nor over a rig clip other than the dodge's own (dash / dash2): the flip is presentation
# and never cuts the player's own action. The glow starts either way.
execute if score @s pmMoveLock matches 1 run return run function rlk:char/motion/beat/tint_on
execute if score @s pmActive matches 1 unless data storage rlk:player_motion active{clip:"dash"} unless data storage rlk:player_motion active{clip:"dash2"} run return run function rlk:char/motion/beat/tint_on
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
