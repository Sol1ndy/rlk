# sweep clock 32
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^ ^0.4 ^2.2 run particle minecraft:dust{color:[0.929f,0.765f,0.043f],scale:0.8} ~ ~ ~ 2.2 0.4 1.2 0 10 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^ ^0.1 ^2.2 run particle minecraft:dust{color:[0.345f,0.333f,0.259f],scale:1.8} ~ ~ ~ 2 0.02 1.2 0 16 force @a[tag=player]
# the low glide to her right (G = P + 4.5 b sideways, body clamp), 10 t
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p13g]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^-4.5 ^ ^ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p13","rlk_mb_bf_p13g"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p13g,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_b
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p13g,limit=1] run function rlk:mboss/mv/glide {t:10}
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
