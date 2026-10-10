# Called only for the OLD active clip before motion/stop clears it.
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} run scoreboard players set @s arSk 0
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} run tag @e[tag=rlk_artg] remove rlk_artg
execute if data storage rlk:player_motion active{char:"arle",clip:"skill"} if entity @s[tag=rlk_body] run effect clear @s minecraft:invisibility
execute if data storage rlk:player_motion active{char:"arle",clip:"burst"} run function rlk:char/burst_wind_end
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run function rlk:char/burst_wind_end
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run scoreboard players set @s skBurst 0
execute if data storage rlk:player_motion active{char:"skirk",clip:"burst_metsu"} run kill @e[tag=rlk_skb]
