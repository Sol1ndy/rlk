# @s = body (module tick, before the rig tick): Rotation = start + sign x schedule[t] / 100; off at the
# clip end (the anchor keeps the final yaw).
scoreboard players add #apYawT mb 1
execute if score #apYawC mb matches 1003 if score #apYawT mb matches 10.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1012 if score #apYawT mb matches 140.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1014 if score #apYawT mb matches 130.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1015 if score #apYawT mb matches 127.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1018 if score #apYawT mb matches 20.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1028 if score #apYawT mb matches 92.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1029 if score #apYawT mb matches 224.. run return run scoreboard players set #apYawC mb 0
execute if score #apYawC mb matches 1033 if score #apYawT mb matches 87.. run return run scoreboard players set #apYawC mb 0
execute store result storage rlk:mboss ap.ya.c int 1 run scoreboard players get #apYawC mb
execute store result storage rlk:mboss ap.ya.t int 1 run scoreboard players get #apYawT mb
function rlk:mboss/apep/yaw/get with storage rlk:mboss ap.ya
scoreboard players operation #apYd mb *= #apYawSg mb
scoreboard players operation #apYd mb += #apYaw0 mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apYd mb
