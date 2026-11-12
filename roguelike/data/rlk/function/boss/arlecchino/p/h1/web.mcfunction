# H1 web (@s = body): the web 7.0 b above a point 6 b behind her (else 4 / 2 / 0 b; the floor spot passes mv/ok);
# she runs up the crimson thread to it in 10 t.
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s rotated as @s rotated ~180 0 positioned ^ ^ ^6 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s rotated as @s rotated ~180 0 positioned ^ ^ ^4 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s rotated as @s rotated ~180 0 positioned ^ ^ ^2 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s rotated as @s rotated ~180 0 positioned ^ ^ ^0 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] positioned ~ ~7 ~ run function rlk:mboss/mv/glide {t:10}
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
