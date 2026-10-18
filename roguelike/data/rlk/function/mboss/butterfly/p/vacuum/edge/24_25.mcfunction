# the point 24 b ahead is inside: is 25 b?
execute positioned ^ ^ ^25 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-25 run return run function rlk:mboss/butterfly/p/vacuum/edge/25_25
return run function rlk:mboss/butterfly/p/vacuum/edge/24_24
