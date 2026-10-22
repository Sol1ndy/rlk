# @s = body: the hop-back spot, d b from the player: straight away from the player, else turned round
# the player (+-40, +-80, +-120, 180 deg) until it is inside the safe disc (mv/ok); none -> no hop.
kill @e[type=minecraft:marker,tag=rlk_mb_gd_bk]
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~0 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~40 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~-40 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~80 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~-80 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~120 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~-120 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~180 0 positioned ^ ^ ^6.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_bk"]}
