# Called only for the OLD active clip before motion/stop clears it.
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} run scoreboard players set @s arSk 0
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} run tag @e[tag=rlk_artg] remove rlk_artg
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} if entity @s[tag=rlk_body] run effect clear @s minecraft:invisibility
execute if data storage rlk:player_motion active{char:"arle",clip:"burst"} run function rlk:char/burst_wind_end
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run function rlk:char/burst_wind_end
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run scoreboard players set @s skBurst 0
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run kill @e[tag=rlk_skb]
# Navia: an interrupted aim ends without a shot (the charge is spent only on release); a skill clip cut before its
# shot tick fires the already-spent shot now (char/navia/shot_cancel); an interrupted burst ends the wind-up.
execute if data storage rlk:player_motion active{char:"navia",clip:"skill_aim_in"} unless score #nvKeep tmp matches 1 if score @s nvA matches 1.. run function rlk:char/navia/aim_cancel
execute if data storage rlk:player_motion active{char:"navia",clip:"skill_aim"} unless score #nvKeep tmp matches 1 if score @s nvA matches 1.. run function rlk:char/navia/aim_cancel
execute if data storage rlk:player_motion active{char:"navia"} if score @s nvShot matches 1.. run function rlk:char/navia/shot_cancel
execute if data storage rlk:player_motion active{char:"navia",clip:"burst"} run function rlk:char/burst_wind_end
