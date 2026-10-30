# O2 (plan 8.2): every 50 t holding a slot: basic_ranged (pivot 0, crown flare 3, open 5-12), the bolt at t12.
execute if score @s apT matches 50.. run function rlk:boss/apep/org/basic/f_start
execute if score @s apT matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^0.55 ^0.75 run function rlk:boss/apep/fx/p/crown_flare
execute if score @s apT matches 3 at @s run function rlk:boss/apep/fx/snd/o2_charge
execute if score @s apT matches 12 run function rlk:boss/apep/org/basic/f_bolt
