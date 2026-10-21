# mstrike #apq31T 36
execute at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,distance=..1,limit=1] run execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.8 run function rlk:boss/apep/u/step_here
execute at @s positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p31l,limit=1] feet rotated ~ 0 run function rlk:boss/apep/fx/p/leaf_pad
execute at @s run function rlk:boss/apep/fx/snd/q1_trail
