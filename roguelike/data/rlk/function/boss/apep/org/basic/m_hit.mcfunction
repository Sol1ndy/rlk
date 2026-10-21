# The O1 strike: the Heart loses (a body-blocking player took the cone instead of nothing: the hazard is the framework's);
# the hit sound and the kit's O1 impact preset at the cone (AP-I2, RREV-6).
execute if entity @s[tag=rlk_mb_ap_buff] run function rlk:boss/apep/heart/sub {v:120}
execute unless entity @s[tag=rlk_mb_ap_buff] run function rlk:boss/apep/heart/sub {v:60}
execute at @s run function rlk:boss/apep/fx/snd/o1_attack
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^1.6 run function rlk:boss/apep/fx/p/o1_hit
