# @s = body: the running pattern (#cpT = its clock).
scoreboard players add #cpT mb 1
execute if score #cpPat mb matches 1 run function rlk:mboss/cproto/p/1
execute if score #cpPat mb matches 2 run function rlk:mboss/cproto/p/2
execute if score #cpPat mb matches 3 run function rlk:mboss/cproto/p/3
