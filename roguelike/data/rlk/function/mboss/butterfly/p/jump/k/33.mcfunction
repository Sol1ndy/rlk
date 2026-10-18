# jump clock 33
function rlk:mboss/butterfly/rig_stub/face/track
function rlk:mboss/butterfly/rig_stub/face/player
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p2a]
scoreboard players set #bfDMax mb 35
scoreboard players set #bfDKeep mb 8
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p2a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p2a] remove rlk_mb_bf_dest
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p2a,limit=1] run function rlk:mboss/mv/glide {t:22}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/p/spiral_jump
function rlk:mboss/butterfly/fx/snd/spiral_jump
playsound minecraft:entity.breeze.whirl hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~0 ~0.3 ~1.4 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~0 ~0.3 ~-1.4 0 0 0 0 1 force @a[tag=player]
