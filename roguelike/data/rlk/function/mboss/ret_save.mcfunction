# Return point = rlk_safe (last solid footing in the dungeon), else the body; facing from the player.
execute store result storage rlk:mboss ret.x double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result storage rlk:mboss ret.y double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100
execute store result storage rlk:mboss ret.z double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.x double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[0] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.y double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[1] 100
execute if entity @e[tag=rlk_safe,limit=1] store result storage rlk:mboss ret.z double 0.01 run data get entity @e[tag=rlk_safe,limit=1] Pos[2] 100
execute store result storage rlk:mboss ret.yaw float 0.01 run data get entity @a[tag=player,limit=1] Rotation[0] 100
execute store result storage rlk:mboss ret.pitch float 0.01 run data get entity @a[tag=player,limit=1] Rotation[1] 100
data modify storage rlk:mboss ret.dim set value "minecraft:overworld"
data modify storage rlk:mboss ret.dim set from entity @a[tag=player,limit=1] Dimension
