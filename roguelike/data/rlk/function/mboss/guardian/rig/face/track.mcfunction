# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 gdRigY 36000
execute store result score #yaw gdRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw gdRigY 18000
scoreboard players operation #yaw gdRigY %= #c36000 gdRigY
execute if score #yaw gdRigY matches ..-1 run scoreboard players add #yaw gdRigY 36000
scoreboard players remove #yaw gdRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_gd_face"]}
execute as @e[type=marker,tag=rlk_mb_gd_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT gdRigY run data get entity @e[type=marker,tag=rlk_mb_gd_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_gd_face]
scoreboard players operation #yawT gdRigY -= #yaw gdRigY
execute if score #yawT gdRigY matches 18000.. run scoreboard players remove #yawT gdRigY 36000
execute if score #yawT gdRigY matches ..-18001 run scoreboard players add #yawT gdRigY 36000
execute if score #yawT gdRigY matches 1201.. run scoreboard players set #yawT gdRigY 1200
execute if score #yawT gdRigY matches ..-1201 run scoreboard players set #yawT gdRigY -1200
scoreboard players operation #yaw gdRigY += #yawT gdRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw gdRigY
