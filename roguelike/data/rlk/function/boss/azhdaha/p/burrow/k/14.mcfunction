# burrow #azPT 14
function rlk:boss/azhdaha/fx/snd/burrow_dive
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/dig/1
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/dig/2
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/dig/3
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/dig/4
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/dig/5
execute positioned ^ ^ ^3.0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9g"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p9g,limit=1] run function rlk:boss/azhdaha/u/clamp_r {r:12}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p9g,limit=1] run function rlk:mboss/mv/glide {t:22}
kill @e[tag=rlk_mb_az_p9g]
