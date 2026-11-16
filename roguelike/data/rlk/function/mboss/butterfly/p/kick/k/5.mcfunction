# kick clock 5
function rlk:mboss/butterfly/rig/face/track
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 run particle minecraft:wax_off ^ ^0.1 ^0.6 0.5 0.05 0.5 0 4 force @a[tag=player]
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] rotated ~ 0 run particle minecraft:dust{color:[0.898f,0.984f,0.784f],scale:0.8} ^ ^0.1 ^0.6 0.5 0.1 0.5 0 6 force @a[tag=player]
