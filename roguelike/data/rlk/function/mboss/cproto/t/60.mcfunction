# test 60 (@s = body, at it)
scoreboard players set #hzAct mb 80
scoreboard players set #hzRearm mb 10
execute at @s positioned ~ 201 ~4 run function rlk:mboss/hz/disc {r:20,tell:12,dmg:30}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:mboss/hz/extend {n:40}
