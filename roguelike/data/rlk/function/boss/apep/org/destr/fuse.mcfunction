# The fuse: pulses at [0, 9, 18, 27, 36, 40, 44, 48, 52], the suck at 56, the blast at 61.
execute if score @s apT matches 9 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 18 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 27 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 36 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 40 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 44 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 48 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 52 at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run function rlk:boss/apep/fx/p/fuse_pulse
execute if score @s apT matches 56 at @s run function rlk:boss/apep/fx/snd/o7_suck
execute if score @s apT matches 61.. run function rlk:boss/apep/org/destr/blast
