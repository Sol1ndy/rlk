# @s = body (Gen.yaw_rebase(); AP-I2, requests RP1-1 / RP3-1): a pattern turned the body inside a yaw clip; the
# driver keeps that facing: #apYaw0 = Rotation x 100 - sign x schedule[t], t = the tick it shows next (#apYawT + 1).
execute unless score #apYawC mb matches 1.. run return 0
execute store result score #apYaw0 mb run data get entity @s Rotation[0] 100
execute store result storage rlk:mboss ap.ya.c int 1 run scoreboard players get #apYawC mb
scoreboard players operation #apYd mb = #apYawT mb
scoreboard players add #apYd mb 1
execute store result storage rlk:mboss ap.ya.t int 1 run scoreboard players get #apYd mb
scoreboard players set #apYd mb 0
function rlk:boss/apep/yaw/get with storage rlk:mboss ap.ya
scoreboard players operation #apYd mb *= #apYawSg mb
scoreboard players operation #apYaw0 mb -= #apYd mb
