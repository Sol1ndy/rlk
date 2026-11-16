# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 bfRigY 36000
execute store result score #yaw bfRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw bfRigY 18000
scoreboard players operation #yaw bfRigY %= #c36000 bfRigY
execute if score #yaw bfRigY matches ..-1 run scoreboard players add #yaw bfRigY 36000
scoreboard players remove #yaw bfRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_bf_face"]}
execute as @e[type=marker,tag=rlk_mb_bf_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT bfRigY run data get entity @e[type=marker,tag=rlk_mb_bf_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_bf_face]
scoreboard players operation #yawT bfRigY -= #yaw bfRigY
execute if score #yawT bfRigY matches 18000.. run scoreboard players remove #yawT bfRigY 36000
execute if score #yawT bfRigY matches ..-18001 run scoreboard players add #yawT bfRigY 36000
execute if score #yawT bfRigY matches 1201.. run scoreboard players set #yawT bfRigY 1200
execute if score #yawT bfRigY matches ..-1201 run scoreboard players set #yawT bfRigY -1200
scoreboard players operation #yaw bfRigY += #yawT bfRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bfRigY
