# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 rdRigY 36000
execute store result score #yaw rdRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw rdRigY 18000
scoreboard players operation #yaw rdRigY %= #c36000 rdRigY
execute if score #yaw rdRigY matches ..-1 run scoreboard players add #yaw rdRigY 36000
scoreboard players remove #yaw rdRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_rd_face"]}
execute as @e[type=marker,tag=rlk_rd_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT rdRigY run data get entity @e[type=marker,tag=rlk_rd_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_rd_face]
scoreboard players operation #yawT rdRigY -= #yaw rdRigY
execute if score #yawT rdRigY matches 18000.. run scoreboard players remove #yawT rdRigY 36000
execute if score #yawT rdRigY matches ..-18001 run scoreboard players add #yawT rdRigY 36000
execute if score #yawT rdRigY matches 1201.. run scoreboard players set #yawT rdRigY 1200
execute if score #yawT rdRigY matches ..-1201 run scoreboard players set #yawT rdRigY -1200
scoreboard players operation #yaw rdRigY += #yawT rdRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw rdRigY
