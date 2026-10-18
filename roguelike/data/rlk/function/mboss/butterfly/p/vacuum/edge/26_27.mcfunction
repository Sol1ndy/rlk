# the point 26 b ahead is inside: is 27 b?
execute positioned ^ ^ ^27 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-27 run return run function rlk:mboss/butterfly/p/vacuum/edge/27_27
return run function rlk:mboss/butterfly/p/vacuum/edge/26_26
