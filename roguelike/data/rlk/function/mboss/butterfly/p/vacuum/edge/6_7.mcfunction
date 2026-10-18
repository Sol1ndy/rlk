# the point 6 b ahead is inside: is 7 b?
execute positioned ^ ^ ^7 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-7 run return run function rlk:mboss/butterfly/p/vacuum/edge/7_7
return run function rlk:mboss/butterfly/p/vacuum/edge/6_6
