# release clock 44
# the wings wrap into the pod: the core glow grows inside it, inward streaks; pressure builds
execute rotated as @s rotated ~ 0 positioned ^0 ^3.24 ^0.23 run function rlk:mboss/butterfly/fx/p/rel_pod
function rlk:mboss/butterfly/fx/snd/release_wrap
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.5 0.9 0.17
