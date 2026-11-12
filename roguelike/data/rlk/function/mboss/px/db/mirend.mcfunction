# @s = a proxy holding mirEnd (the mirror item (items/proc/mirror)): the body takes the larger value, the proxy drops it.
scoreboard players operation @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] mirEnd > @s mirEnd
scoreboard players set @s mirEnd 0
