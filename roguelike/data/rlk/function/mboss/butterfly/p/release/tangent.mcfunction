# @s = the release marker R (beyond r 16): back on L0, then 4 b along the wall tangent, the way that
# takes it farther from her (two candidates; the farther one from the body stays).
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p15k]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15l,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~90 0 positioned ^ ^ ^4 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p15k","rlk_mb_bf_kept"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15l,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~-90 0 positioned ^ ^ ^4 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p15k","rlk_mb_bf_kept"]}
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p15k,sort=furthest,limit=1] run tp @s ~ ~ ~
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p15k]
