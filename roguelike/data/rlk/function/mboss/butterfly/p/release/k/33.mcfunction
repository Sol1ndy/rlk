# release clock 33
# the wings wrap into the pod (the rig's pod prop at the core anchor until the snap, rig API section 6.1):
# the core glow grows inside it, inward streaks; pressure builds
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]
execute rotated as @s rotated ~ 0 positioned ^0 ^4.811 ^0.415 run function rlk:mboss/butterfly/rig/prop/pod
execute rotated as @s rotated ~ 0 positioned ^0 ^4.811 ^0.415 run function rlk:mboss/butterfly/fx/p/rel_pod
function rlk:mboss/butterfly/fx/snd/release_wrap
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.5 0.9 0.17
