# The nova hit (the hazard strikes this tick).
execute at @s positioned ~ ~0.2 ~ run function rlk:boss/tachy/fx/p/shock_ring {r:200}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/nova_flash
execute at @s run function rlk:boss/tachy/fx/snd/nova_blast
