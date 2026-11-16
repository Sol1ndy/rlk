# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 knRigY 36000
execute store result score #yaw knRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw knRigY 18000
scoreboard players operation #yaw knRigY %= #c36000 knRigY
execute if score #yaw knRigY matches ..-1 run scoreboard players add #yaw knRigY 36000
scoreboard players remove #yaw knRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_kn_face"]}
execute as @e[type=marker,tag=rlk_kn_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT knRigY run data get entity @e[type=marker,tag=rlk_kn_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_kn_face]
scoreboard players operation #yawT knRigY -= #yaw knRigY
execute if score #yawT knRigY matches 18000.. run scoreboard players remove #yawT knRigY 36000
execute if score #yawT knRigY matches ..-18001 run scoreboard players add #yawT knRigY 36000
execute if score #yawT knRigY matches 1201.. run scoreboard players set #yawT knRigY 1200
execute if score #yawT knRigY matches ..-1201 run scoreboard players set #yawT knRigY -1200
scoreboard players operation #yaw knRigY += #yawT knRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw knRigY
