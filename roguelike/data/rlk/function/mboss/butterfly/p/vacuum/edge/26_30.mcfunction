# the point 26 b ahead is inside: is 28 b?
execute positioned ^ ^ ^28 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-28 run return run function rlk:mboss/butterfly/p/vacuum/edge/28_30
return run function rlk:mboss/butterfly/p/vacuum/edge/26_27
