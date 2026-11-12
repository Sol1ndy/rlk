# Macro {x, z} (@s = a missile): its apex marker rlk_mb_fg_p4a.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p4a]
$execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^$(x) ^16 ^$(z) run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p4","rlk_mb_fg_p4a"]}
