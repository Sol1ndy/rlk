# release clock 91
function rlk:mboss/butterfly/rig_stub/face/track
# the shrunken flat lime wings shatter
execute rotated as @s rotated ~ 0 positioned ^ ^2.8 ^-0.4 run function rlk:mboss/butterfly/fx/p/wing_shatter
function rlk:mboss/butterfly/fx/snd/wing_shatter
execute rotated as @s rotated ~ 0 run particle minecraft:block{block_state:"minecraft:lime_stained_glass"} ^ ^3 ^-0.4 2 1 1 0 20 force @a[tag=player]
