# @s = body (t18): the four spike points (plan 5 P4), clamped inside r 27: B = lockv (lead 28),
# A = the head column + 3 b toward B, C / D = B + 4 / 8 b along the player's velocity
# (|v| > 80 mb/t) else along head -> B.
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:28}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p4b]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_kept
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p4b
tag @e[type=minecraft:marker,tag=rlk_mb_az_p4b] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p4b] remove rlk_mb_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p4b] add rlk_mb_az_p4
tag @e[type=minecraft:marker,tag=rlk_mb_az_p4b] add rlk_mb_az_pat
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] run function rlk:boss/azhdaha/u/clamp_r {r:27}
kill @e[type=minecraft:marker,tag=rlk_mb_az_p4t]
execute rotated as @s rotated ~ 0 positioned ^ ^ ^4.3 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4t","rlk_mb_az_p4hd"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4hd,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] feet rotated ~ 0 positioned ^ ^ ^3 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4a"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4t","rlk_mb_az_p4dir"]}
execute if score #mbV mb matches 81.. run function rlk:boss/azhdaha/p/spikes/vdir
execute unless score #mbV mb matches 81.. as @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p4hd,limit=1] feet rotated ~180 0 run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] positioned ^ ^ ^4 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4c"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] positioned ^ ^ ^8 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4d"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p4a,limit=1] run function rlk:boss/azhdaha/u/clamp_r {r:27}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p4c,limit=1] run function rlk:boss/azhdaha/u/clamp_r {r:27}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p4d,limit=1] run function rlk:boss/azhdaha/u/clamp_r {r:27}
kill @e[type=minecraft:marker,tag=rlk_mb_az_p4t]
