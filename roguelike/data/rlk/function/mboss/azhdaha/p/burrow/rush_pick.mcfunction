# @s = body: the breach point (rush #aq9N) and the rush hazard there (own group, tell 20, 21 t of hits)
kill @e[tag=rlk_mb_az_p9b]
execute unless score #aq9N mb matches 2 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^6.0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9b"]}
execute if score #aq9N mb matches 2 unless score #aq9E mb matches 1 at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^6.0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9b"]}
execute if score #aq9N mb matches 2 if score #aq9E mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9b"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p9b,limit=1] run function rlk:mboss/azhdaha/u/clamp_r {r:24}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p9b,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p9b,limit=1] run function rlk:mboss/azhdaha/p/burrow/rush_hz
