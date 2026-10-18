# strike clock 8
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:dust{color:[0.906f,0.992f,0.667f],scale:0.8} ~ ~ ~ 0.2 0.2 0.2 0 2 force @a[tag=player]
# the swoop: glide to H (7 t), the dive whoosh
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p11h,limit=1] run function rlk:mboss/mv/glide {t:7}
function rlk:mboss/butterfly/fx/snd/wing_dive
