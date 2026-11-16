# K stage pl: tick 0 (@s = body).
scoreboard players set #k_s tk 5
scoreboard players set #k_c tk 0
kill @e[type=minecraft:marker,tag=rlk_tk_klock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_k","rlk_tk_air","rlk_tk_klock"]}
scoreboard players set #k_n tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] unless function rlk:boss/tachy/p/k/u/fit run kill @s
execute unless entity @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] positioned as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_k","rlk_tk_air","rlk_tk_klock"]}
function rlk:boss/tachy/rig/play/k_plunge
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] run function rlk:boss/tachy/fx/p/sky_arcs {r:35,t:16}
execute at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] positioned ~ ~6 ~ run function rlk:boss/tachy/fx/snd/sky_arcs
