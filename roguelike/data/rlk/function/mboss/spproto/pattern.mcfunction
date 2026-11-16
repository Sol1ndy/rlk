# @s = body: the running pattern (#spT = its clock).
scoreboard players add #spT mb 1
execute if score #spPat mb matches 1 run function rlk:mboss/spproto/p/1
execute if score #spPat mb matches 2 run function rlk:mboss/spproto/p/2
