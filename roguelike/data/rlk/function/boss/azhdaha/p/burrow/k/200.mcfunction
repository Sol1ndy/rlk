# burrow #azPT 200
execute unless score #aq9E mb matches 1 run function rlk:boss/azhdaha/p/burrow/final_lock
execute if score #aq9E mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p9","rlk_mb_az_p9m","rlk_mb_az_p9e"]}
