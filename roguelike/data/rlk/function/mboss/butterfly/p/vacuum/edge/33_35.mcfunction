# the point 33 b ahead is inside: is 34 b?
execute positioned ^ ^ ^34 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-34 run return run function rlk:mboss/butterfly/p/vacuum/edge/34_35
return run function rlk:mboss/butterfly/p/vacuum/edge/33_33
