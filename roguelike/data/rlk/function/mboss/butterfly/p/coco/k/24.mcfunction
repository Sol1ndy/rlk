# coco clock 24
function rlk:mboss/butterfly/rig/face/track
execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/toward {d:0.12}
execute rotated as @s rotated ~ 0 positioned ^0 ^3.156 ^0.428 as @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod] run tp @s ~ ~ ~ ~ ~
