# the point 36 b ahead is inside: is 38 b?
execute positioned ^ ^ ^38 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-38 run return run function rlk:mboss/butterfly/p/vacuum/edge/38_40
return run function rlk:mboss/butterfly/p/vacuum/edge/36_37
