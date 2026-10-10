# 체험 방 (@s = 플레이어)
function rlk:lobby/leave
function rlk:lobby/tp {x:"122.5",y:"193",z:"49.5",yaw:"0"}
scoreboard players set @s lobRoom 4
execute store result score #t lob if entity @e[tag=rlk_dummy,tag=!rlk_tutE]
execute unless score #t lob matches 4 run function rlk:lobby/try/dummies
function rlk:lobby/try/labels
