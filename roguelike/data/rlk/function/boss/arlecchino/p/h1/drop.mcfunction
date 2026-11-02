# H1 drop (@s = body): she drops to 3 b in front of the player on the player -> web line (else 4.5 / 2 b; mv/ok),
# facing the player, over 8 t.
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^4.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^2 positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s positioned ~ 201 ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_dp"]}
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run function rlk:mboss/mv/glide {t:8}
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
function rlk:mboss/mv/face
