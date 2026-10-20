# The tail falls flat.
playsound minecraft:block.deepslate.break hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
playsound minecraft:entity.ravager.step hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^-9 run function rlk:mboss/azhdaha/fx/p/dust
