# W2 stage air tick 60
kill @e[type=minecraft:marker,tag=rlk_tk_w2lock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_w2lock"]}
scoreboard players set #w2_n tk 0
execute as @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] unless function rlk:boss/tachy/p/w2/u/fit run kill @s
execute unless entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] positioned as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_tk_p","rlk_tk_p_w2","rlk_tk_air","rlk_tk_w2lock"]}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
