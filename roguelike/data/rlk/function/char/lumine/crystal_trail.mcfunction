particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:0.7f} ~ ~ ~ 0 0 0 0 1
particle minecraft:snowflake ~ ~ ~ 0 0 0 0 1
execute positioned ~ ~-1 ~ if entity @e[tag=rlk_ctgt,distance=..1.2] run return 0
execute unless entity @e[tag=rlk_lstar,distance=..13] run return 0
execute positioned ^ ^ ^0.6 run function rlk:char/lumine/crystal_trail
