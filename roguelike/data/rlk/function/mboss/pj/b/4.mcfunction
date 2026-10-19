# Blade half width 0.4 b (reach 0.7 b off the line): 2 points x 3 rows, radius 0.45 b (@s = prop, at and rotated as it).
execute positioned ^-0.25 ^-0.9 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^0.25 ^-0.9 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^-0.25 ^-0.3 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^0.25 ^-0.3 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^-0.25 ^0.3 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
execute positioned ^0.25 ^0.3 ^ if entity @e[tag=rlk_body,distance=..0.451,limit=1] run return run function rlk:mboss/pj/hit
