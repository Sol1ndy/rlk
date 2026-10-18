# the point 4 b ahead is inside: is 5 b?
execute positioned ^ ^ ^5 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-5 run return run function rlk:mboss/butterfly/p/vacuum/edge/5_5
return run function rlk:mboss/butterfly/p/vacuum/edge/4_4
