tag @s remove rlk_agq
execute unless entity @e[tag=rlk_lure,limit=1] run return 0
data merge entity @s {InvulnerableTime:0s}
damage @s 0 minecraft:generic by @e[tag=rlk_lure,limit=1]
