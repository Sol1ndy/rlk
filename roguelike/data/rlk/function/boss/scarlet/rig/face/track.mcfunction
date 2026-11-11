# Turn the anchor toward the look target @e[tag=rlk_body,limit=1] by at most 12 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 hrRigY 36000
execute store result score #yaw hrRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw hrRigY 18000
scoreboard players operation #yaw hrRigY %= #c36000 hrRigY
execute if score #yaw hrRigY matches ..-1 run scoreboard players add #yaw hrRigY 36000
scoreboard players remove #yaw hrRigY 18000
execute facing entity @e[tag=rlk_body,limit=1] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_hr_face"]}
execute as @e[type=marker,tag=rlk_hr_face,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run rotate @s ~ 0
execute store result score #yawT hrRigY run data get entity @e[type=marker,tag=rlk_hr_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_hr_face]
scoreboard players operation #yawT hrRigY -= #yaw hrRigY
execute if score #yawT hrRigY matches 18000.. run scoreboard players remove #yawT hrRigY 36000
execute if score #yawT hrRigY matches ..-18001 run scoreboard players add #yawT hrRigY 36000
execute if score #yawT hrRigY matches 1201.. run scoreboard players set #yawT hrRigY 1200
execute if score #yawT hrRigY matches ..-1201 run scoreboard players set #yawT hrRigY -1200
scoreboard players operation #yaw hrRigY += #yawT hrRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw hrRigY
