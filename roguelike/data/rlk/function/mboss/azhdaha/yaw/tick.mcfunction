# @s = body: the scripted yaw (Rotation = start + sign x schedule[t] / 100); off at the clip end.
scoreboard players add #azYawT mb 1
execute if score #azYawC mb matches 1003 if score #azYawT mb matches 24.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1004 if score #azYawT mb matches 24.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1005 if score #azYawT mb matches 36.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1006 if score #azYawT mb matches 36.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1007 if score #azYawT mb matches 60.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1025 if score #azYawT mb matches 64.. run return run scoreboard players set #azYawC mb 0
execute if score #azYawC mb matches 1026 if score #azYawT mb matches 64.. run return run scoreboard players set #azYawC mb 0
execute store result storage rlk:mboss az.ya.c int 1 run scoreboard players get #azYawC mb
execute store result storage rlk:mboss az.ya.t int 1 run scoreboard players get #azYawT mb
function rlk:mboss/azhdaha/yaw/get with storage rlk:mboss az.ya
scoreboard players operation #azYd mb *= #azYawS mb
scoreboard players operation #azYd mb += #azYaw0 mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #azYd mb
