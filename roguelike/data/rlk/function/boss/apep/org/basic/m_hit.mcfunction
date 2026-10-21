# The O1 strike: the Heart loses (a body-blocking player took the cone instead of nothing: the hazard is the framework's);
# the hit sound and a small hit fx at the cone (TODO(I2) RI1-1: the kit's O1 impact preset).
execute if entity @s[tag=rlk_mb_ap_buff] run function rlk:boss/apep/heart/sub {v:120}
execute unless entity @s[tag=rlk_mb_ap_buff] run function rlk:boss/apep/heart/sub {v:60}
execute at @s run function rlk:boss/apep/fx/snd/o1_attack
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^1.6 run particle minecraft:composter ~ ~ ~ 0.35 0.25 0.35 0 8 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^1.6 run particle minecraft:crit ~ ~ ~ 0.25 0.2 0.25 0.1 5 force @a[tag=player]
