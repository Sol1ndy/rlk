# L stage dv: tick 0 (@s = body).
scoreboard players set #l_s tk 3
scoreboard players set #l_c tk 0
kill @e[type=minecraft:marker,tag=rlk_tk_llock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_l","rlk_tk_air","rlk_tk_llock"]}
scoreboard players set #l_n tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] unless function rlk:boss/tachy/p/l/u/fit run kill @s
execute unless entity @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] positioned as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_l","rlk_tk_air","rlk_tk_llock"]}
tag @s remove rlk_mb_inv
function rlk:boss/tachy/rig/play/dive
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_tk_llock,limit=1] run function rlk:mboss/mv/glide {t:10}
execute at @s run function rlk:boss/tachy/fx/snd/dive
