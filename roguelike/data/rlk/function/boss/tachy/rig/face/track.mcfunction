# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 tkRigY 36000
execute store result score #yaw tkRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw tkRigY 18000
scoreboard players operation #yaw tkRigY %= #c36000 tkRigY
execute if score #yaw tkRigY matches ..-1 run scoreboard players add #yaw tkRigY 36000
scoreboard players remove #yaw tkRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_tk_face"]}
execute as @e[type=marker,tag=rlk_tk_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT tkRigY run data get entity @e[type=marker,tag=rlk_tk_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_tk_face]
scoreboard players operation #yawT tkRigY -= #yaw tkRigY
execute if score #yawT tkRigY matches 18000.. run scoreboard players remove #yawT tkRigY 36000
execute if score #yawT tkRigY matches ..-18001 run scoreboard players add #yawT tkRigY 36000
execute if score #yawT tkRigY matches 1201.. run scoreboard players set #yawT tkRigY 1200
execute if score #yawT tkRigY matches ..-1201 run scoreboard players set #yawT tkRigY -1200
scoreboard players operation #yaw tkRigY += #yawT tkRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw tkRigY
