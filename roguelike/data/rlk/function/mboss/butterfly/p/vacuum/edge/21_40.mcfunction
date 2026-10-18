# the point 21 b ahead is inside: is 31 b?
execute positioned ^ ^ ^31 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-31 run return run function rlk:mboss/butterfly/p/vacuum/edge/31_40
return run function rlk:mboss/butterfly/p/vacuum/edge/21_30
