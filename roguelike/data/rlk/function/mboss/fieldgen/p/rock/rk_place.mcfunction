# [c_rocks] Macro {a, d} (@s = body, at it): the burst point d b from the body at the bearing to the player turned
# by a degrees, on the floor, pulled into the walk disc.
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p6w]
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~$(a) 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p6","rlk_mb_fg_p6w"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p6w,limit=1] run function rlk:mboss/fieldgen/u/clamp_w
