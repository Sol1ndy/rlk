# Fallback return point: this zone marker (@s).
execute store result storage rlk:mboss ret.x double 0.01 run data get entity @s Pos[0] 100
execute store result storage rlk:mboss ret.y double 0.01 run data get entity @s Pos[1] 100
execute store result storage rlk:mboss ret.z double 0.01 run data get entity @s Pos[2] 100
data modify storage rlk:mboss ret.yaw set value 0.0f
data modify storage rlk:mboss ret.pitch set value 0.0f
data modify storage rlk:mboss ret.dim set value "minecraft:overworld"
