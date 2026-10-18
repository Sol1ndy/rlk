# the point 31 b ahead is inside: is 33 b?
execute positioned ^ ^ ^33 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-33 run return run function rlk:mboss/butterfly/p/vacuum/edge/33_35
return run function rlk:mboss/butterfly/p/vacuum/edge/31_32
