# @s = player, on the contact tick of a perfect parry (player/def/beat/start_p): the deflect -> lunge freeze -> ready guard motion
# (clip pparry; ref_pd.md 4) and the weapon's yellow-white glow. Rig characters play their clip, mannequin characters the stand-in rig.
# A rig character that has already started another action since the F (an attack clip, a skill) keeps it: only the guard clip
# or no clip gives way to the lunge. The weapon glows either way.
execute if score @s pmActive matches 1 unless data storage rlk:player_motion active{clip:"guard"} unless data storage rlk:player_motion active{clip:"pparry"} unless data storage rlk:player_motion active{clip:"pparry_i"} unless data storage rlk:player_motion active{clip:"pdodge"} unless data storage rlk:player_motion active{clip:"pdodge_i"} unless data storage rlk:player_motion active{clip:"dash"} unless data storage rlk:player_motion active{clip:"dash_l"} unless data storage rlk:player_motion active{clip:"dash_b"} unless data storage rlk:player_motion active{clip:"dash2"} run return run function rlk:char/motion/beat/wglow_on
execute if score #charN tmp matches 5 unless score @s arM matches 1.. run function rlk:char/motion/start {char:"arle",clip:"pparry"}
execute if score #charN tmp matches 5 if score @s arM matches 1.. run function rlk:char/motion/start {char:"arle",clip:"pparry_i"}
execute if score #charN tmp matches 3 unless score @s skM matches 1.. run function rlk:char/motion/start {char:"skirk",clip:"pparry"}
execute if score #charN tmp matches 3 if score @s skM matches 1.. run function rlk:char/motion/start {char:"skirk",clip:"pparry_i"}
execute if score #charN tmp matches 6 run function rlk:char/motion/start {char:"navia",clip:"pparry"}
execute if data storage rlk:player_motion active{clip:"pparry"} run function rlk:char/motion/beat/face
execute if data storage rlk:player_motion active{clip:"pparry_i"} run function rlk:char/motion/beat/face
execute if score #charN tmp matches 1 run function rlk:char/motion/lite/start_p
execute if score #charN tmp matches 4 run function rlk:char/motion/lite/start_p
execute if score #charN tmp matches 7 run function rlk:char/motion/lite/start_p
execute if score #charN tmp matches 8 run function rlk:char/motion/lite/start_p
function rlk:char/motion/beat/wglow_on
