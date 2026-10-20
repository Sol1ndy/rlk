# One rock point (clamped into the walk disc): its hazard and its falling prop.
summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9rn"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p9rn,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p9rn,limit=1] run function rlk:mboss/azhdaha/p/burrow/rock_mk
tag @e[tag=rlk_mb_az_p9rn] add rlk_mb_az_p9rk
tag @e[tag=rlk_mb_az_p9rn] remove rlk_mb_az_p9rn
