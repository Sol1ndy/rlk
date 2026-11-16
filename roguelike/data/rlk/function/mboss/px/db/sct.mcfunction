# @s = a proxy holding scT (superconduct (element/run/supercond)): the body takes the larger value, the proxy drops it.
scoreboard players operation @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] scT > @s scT
scoreboard players set @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] elAct 1
scoreboard players set @s scT 0
