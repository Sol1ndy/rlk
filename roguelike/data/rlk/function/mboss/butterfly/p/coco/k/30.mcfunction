# coco clock 30
function rlk:mboss/butterfly/rig/face/track
# the cocoon ball (wings wrapped, drifting toward the player): lime glow inside, swirling rustle
execute rotated as @s rotated ~ 0 positioned ^ ^3.0 ^ run function rlk:mboss/butterfly/fx/p/cocoon_ball
function rlk:mboss/butterfly/fx/snd/cocoon_ball
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]
execute rotated as @s rotated ~ 0 positioned ^ ^3.0 ^ run function rlk:mboss/butterfly/rig/prop/pod
execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.12}
