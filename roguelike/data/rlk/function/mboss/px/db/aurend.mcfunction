# @s = a proxy holding aurEnd (Yoimiya's aura (char/yoimiya/rocket_boom, aur_move)): the body takes the larger value, the proxy drops it.
scoreboard players operation @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] aurEnd > @s aurEnd
scoreboard players set @s aurEnd 0
