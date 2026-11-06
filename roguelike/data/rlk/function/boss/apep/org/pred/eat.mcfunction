# The nearest held basic is eaten (silently); none left (killed meanwhile): no burst, it circles un-empowered.
execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4] run return run function rlk:boss/apep/org/pred/circle_go
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4,sort=nearest,limit=1] run function rlk:boss/apep/org/basic/swallowed
tag @s add rlk_mb_ap_pemp
execute at @s run function rlk:boss/apep/fx/snd/o6_gulp
execute at @s run function rlk:boss/apep/fx/snd/o6_bud
