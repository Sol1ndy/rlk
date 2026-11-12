# Turn the anchor toward the nearest player by at most 2 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 azRigY 36000
execute store result score #yaw azRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw azRigY 18000
scoreboard players operation #yaw azRigY %= #c36000 azRigY
execute if score #yaw azRigY matches ..-1 run scoreboard players add #yaw azRigY 36000
scoreboard players remove #yaw azRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_az_face"]}
execute as @e[type=marker,tag=rlk_mb_az_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT azRigY run data get entity @e[type=marker,tag=rlk_mb_az_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_az_face]
scoreboard players operation #yawT azRigY -= #yaw azRigY
execute if score #yawT azRigY matches 18000.. run scoreboard players remove #yawT azRigY 36000
execute if score #yawT azRigY matches ..-18001 run scoreboard players add #yawT azRigY 36000
execute if score #yawT azRigY matches 201.. run scoreboard players set #yawT azRigY 200
execute if score #yawT azRigY matches ..-201 run scoreboard players set #yawT azRigY -200
scoreboard players operation #yaw azRigY += #yawT azRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw azRigY
