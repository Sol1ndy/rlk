# Turn the anchor toward the nearest player by at most 4 degrees per call. @s = rig anchor.
# Both yaws are normalised into [-180, 180) first, so the stored yaw never drifts past one turn.
scoreboard players set #c36000 fgRigY 36000
execute store result score #yaw fgRigY run data get entity @s Rotation[0] 100
scoreboard players add #yaw fgRigY 18000
scoreboard players operation #yaw fgRigY %= #c36000 fgRigY
execute if score #yaw fgRigY matches ..-1 run scoreboard players add #yaw fgRigY 36000
scoreboard players remove #yaw fgRigY 18000
execute facing entity @p[gamemode=!spectator] feet run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_aux","rlk_mb_fg_face"]}
execute as @e[type=marker,tag=rlk_mb_fg_face,limit=1] at @s facing entity @p[gamemode=!spectator] feet run rotate @s ~ 0
execute store result score #yawT fgRigY run data get entity @e[type=marker,tag=rlk_mb_fg_face,limit=1] Rotation[0] 100
kill @e[type=marker,tag=rlk_mb_fg_face]
scoreboard players operation #yawT fgRigY -= #yaw fgRigY
execute if score #yawT fgRigY matches 18000.. run scoreboard players remove #yawT fgRigY 36000
execute if score #yawT fgRigY matches ..-18001 run scoreboard players add #yawT fgRigY 36000
execute if score #yawT fgRigY matches 401.. run scoreboard players set #yawT fgRigY 400
execute if score #yawT fgRigY matches ..-401 run scoreboard players set #yawT fgRigY -400
scoreboard players operation #yaw fgRigY += #yawT fgRigY
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw fgRigY
