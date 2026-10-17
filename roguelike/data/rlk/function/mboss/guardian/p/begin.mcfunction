# @s = body. First tick of the slot pattern #gdPat: clock 0, start function (plays its clip).
scoreboard players set #gdPNew mb 0
scoreboard players set #gdPT mb 0
scoreboard players set #gdPEnd mb 0
scoreboard players set #gdPMax mb 200
execute if score #gdPat mb matches 1 run scoreboard players set #gdPMax mb 95
execute if score #gdPat mb matches 2 run scoreboard players set #gdPMax mb 80
execute if score #gdPat mb matches 3 run scoreboard players set #gdPMax mb 74
execute if score #gdPat mb matches 4 run scoreboard players set #gdPMax mb 99
execute if score #gdPat mb matches 5 run scoreboard players set #gdPMax mb 105
execute if score #gdPat mb matches 11 run scoreboard players set #gdPMax mb 48
execute if score #gdPat mb matches 12 run scoreboard players set #gdPMax mb 54
execute if score #gdPat mb matches 13 run scoreboard players set #gdPMax mb 120
execute if score #gdSt mb matches 1 run function rlk:mboss/guardian/hud/sub_pattern
function rlk:mboss/guardian/p/start
