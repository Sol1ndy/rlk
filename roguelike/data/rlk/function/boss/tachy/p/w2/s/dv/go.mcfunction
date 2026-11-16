# W2 stage dv: tick 0 (@s = body).
scoreboard players set #w2_s tk 3
scoreboard players set #w2_c tk 0
function rlk:boss/tachy/rig/play/w2_dive
execute at @s run function rlk:boss/tachy/fx/snd/dive
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
kill @e[type=minecraft:marker,tag=rlk_tk_w2p]
execute at @s positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] feet rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_w2p"]}
execute at @s positioned ~ 201 ~ facing entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] feet rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_tk_w2p,limit=1] run tp @s ~ ~ ~ ~ 0
scoreboard players set #w2_n tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_w2p,limit=1] at @s run function rlk:boss/tachy/p/w2/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_tk_w2p,limit=1] run function rlk:mboss/mv/glide {t:6}
