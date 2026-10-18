# the point 39 b ahead is inside: is 40 b?
execute positioned ^ ^ ^40 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-40 run return run function rlk:mboss/butterfly/p/vacuum/edge/40_40
return run function rlk:mboss/butterfly/p/vacuum/edge/39_39
