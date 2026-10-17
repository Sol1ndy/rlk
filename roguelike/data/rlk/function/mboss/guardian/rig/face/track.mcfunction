# Turn the anchor toward the nearest player by at most 12 degrees per call. @s = rig anchor.
execute store result score #yaw gdRigY run data get entity @s Rotation[0] 100
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_gd_face"]}
execute as @e[type=marker,tag=rlk_mb_gd_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT gdRigY run data get entity @e[type=marker,tag=rlk_mb_gd_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_gd_face]
scoreboard players operation #yawT gdRigY -= #yaw gdRigY
execute if score #yawT gdRigY matches 18000.. run scoreboard players remove #yawT gdRigY 36000
execute if score #yawT gdRigY matches ..-18000 run scoreboard players add #yawT gdRigY 36000
execute if score #yawT gdRigY matches 1201.. run scoreboard players set #yawT gdRigY 1200
execute if score #yawT gdRigY matches ..-1201 run scoreboard players set #yawT gdRigY -1200
scoreboard players operation #yaw gdRigY += #yawT gdRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw gdRigY
