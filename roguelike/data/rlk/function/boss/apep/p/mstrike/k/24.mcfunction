# mstrike #apq31T 24
execute at @s unless entity @e[tag=rlk_body,distance=..3,limit=1] run execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.8 run function rlk:boss/apep/u/step_here
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_pad
execute at @s run function rlk:boss/apep/fx/snd/q1_trail
