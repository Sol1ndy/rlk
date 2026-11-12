# Turn the anchor toward the nearest player by at most 2 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 apRigY 36000
execute store result score #yaw apRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw apRigY 18000
scoreboard players operation #yaw apRigY %= #c36000 apRigY
execute if score #yaw apRigY matches ..-1 run scoreboard players add #yaw apRigY 36000
scoreboard players remove #yaw apRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_ap_face"]}
execute as @e[type=marker,tag=rlk_mb_ap_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT apRigY run data get entity @e[type=marker,tag=rlk_mb_ap_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_ap_face]
scoreboard players operation #yawT apRigY -= #yaw apRigY
execute if score #yawT apRigY matches 18000.. run scoreboard players remove #yawT apRigY 36000
execute if score #yawT apRigY matches ..-18001 run scoreboard players add #yawT apRigY 36000
execute if score #yawT apRigY matches 201.. run scoreboard players set #yawT apRigY 200
execute if score #yawT apRigY matches ..-201 run scoreboard players set #yawT apRigY -200
scoreboard players operation #yaw apRigY += #yawT apRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw apRigY
