# Blade half width 0.1 b (reach 0.4 b off the line): 1 points x 3 rows, radius 0.4 b (@s = prop, at and rotated as it).
execute positioned ^0 ^-0.9 ^ if entity @e[tag=rlk_body,distance=..0.401,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^0 ^-0.3 ^ if entity @e[tag=rlk_body,distance=..0.401,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^0 ^0.3 ^ if entity @e[tag=rlk_body,distance=..0.401,limit=1] run return run function rlk:mboss/pj/hit
