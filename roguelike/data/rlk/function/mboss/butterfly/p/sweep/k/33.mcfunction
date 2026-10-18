# sweep clock 33
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^ ^0.5 ^2.0 run particle minecraft:campfire_cosy_smoke ~ ~ ~ 1.5 0.2 1 0.01 3 force @a[tag=player]
playsound minecraft:entity.blaze.burn hostile @a[tag=player] ~ ~ ~ 0.4 0.9 0.13
# the low glide to her right (G = P + 4.5 b sideways, body clamp), 10 t from the rig's glide event
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p13g]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^-4.5 ^ ^ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p13","rlk_mb_bf_p13g"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p13g,limit=1] run function rlk:mboss/butterfly/wx/u/clamp_b
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p13g,limit=1] run function rlk:mboss/mv/glide {t:10}
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
