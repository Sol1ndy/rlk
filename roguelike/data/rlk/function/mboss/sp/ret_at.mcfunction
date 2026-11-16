# @s = the rift anchor, at it, rotated toward the room centre (pitch 0).
summon minecraft:marker ^ ^ ^1.2 {Tags:["rlk_room","rlk_sp_ret"]}
execute positioned ^ ^ ^2 if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass unless block ~ ~-1 ~ #rlk:dash_pass run tp @e[type=minecraft:marker,tag=rlk_sp_ret,limit=1] ~ ~ ~
execute store result storage rlk:mboss ret.x double 0.01 run data get entity @e[type=minecraft:marker,tag=rlk_sp_ret,limit=1] Pos[0] 100
execute store result storage rlk:mboss ret.y double 0.01 run data get entity @e[type=minecraft:marker,tag=rlk_sp_ret,limit=1] Pos[1] 100
execute store result storage rlk:mboss ret.z double 0.01 run data get entity @e[type=minecraft:marker,tag=rlk_sp_ret,limit=1] Pos[2] 100
execute store result storage rlk:mboss ret.yaw float 0.01 run data get entity @s Rotation[0] 100
data modify storage rlk:mboss ret.pitch set value 0.0f
data modify storage rlk:mboss ret.dim set value "minecraft:overworld"
kill @e[type=minecraft:marker,tag=rlk_sp_ret]
