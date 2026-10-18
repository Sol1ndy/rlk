# the point 31 b ahead is inside: is 36 b?
execute positioned ^ ^ ^36 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..20.7,limit=1] positioned ^ ^ ^-36 run return run function rlk:mboss/butterfly/p/vacuum/edge/36_40
return run function rlk:mboss/butterfly/p/vacuum/edge/31_35
