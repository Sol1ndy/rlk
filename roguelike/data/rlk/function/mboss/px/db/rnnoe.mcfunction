# @s = a proxy holding rnNoE (Ronova's echo window (char/ronova/echo_boom)): the body takes the larger value, the proxy drops it.
scoreboard players operation @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rnNoE > @s rnNoE
scoreboard players set @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] elAct 1
scoreboard players set @s rnNoE 0
