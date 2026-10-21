# absorb1 #azPT 86
execute at @s rotated as @s rotated ~ 0 positioned ^-3.15 ^0 ^2.4 run execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/footfall/1
execute at @s rotated as @s rotated ~ 0 positioned ^-3.15 ^0 ^2.4 run execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/footfall/2
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/snd/footfall/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/snd/footfall/2
