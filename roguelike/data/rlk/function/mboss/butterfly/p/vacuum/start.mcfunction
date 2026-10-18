# H4 광폭한 진공 (clip vacuum). The glint 9: the yaw locked, the lane decal to the wall; the stomp 16;
# the blade at 17 (pj blade hr 1.2, 0.7 b/t -> 0.75, 60 t, no homing; it outlives the
# pattern: p/vacuum/blades from the core ai/state); the backflip 18-34, the landing 38; 1.2 Dendro.
function rlk:mboss/butterfly/rig_stub/face/player
execute at @s rotated as @s rotated ~ 0 positioned ^-0.42 ^0.15 ^0.06 run function rlk:mboss/butterfly/fx/p/vac_crouch
playsound minecraft:block.moss_carpet.step hostile @a[tag=player] ~ ~ ~ 0.4 0.9 0.13
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.886f,0.988f,0.533f],scale:0.8} ^-0.42 ^0.15 ^0.06 0.1 0.15 0.1 0 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.788f,0.949f,0.678f],scale:0.6} ^-0.42 ^0.15 ^0.06 0.1 0.3 0.1 0.01 1 force @a[tag=player]
