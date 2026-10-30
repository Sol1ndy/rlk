# coco clock 22
function rlk:mboss/butterfly/rig/face/track
# the cocoon ball (wings wrapped, drifting toward the player): the rig's closed pod at the core anchor (rig API
# section 6.1: summoned at ball, cleared at ball_open), lime glow inside, swirling rustle
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]
execute rotated as @s rotated ~ 0 positioned ^0 ^3.156 ^0.428 run function rlk:mboss/butterfly/rig/prop/pod
execute rotated as @s rotated ~ 0 positioned ^0 ^3.156 ^0.428 run function rlk:mboss/butterfly/fx/p/cocoon_ball
function rlk:mboss/butterfly/fx/snd/cocoon_ball
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.12}
