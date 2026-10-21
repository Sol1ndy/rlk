# meteor #azCT 27
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p32","rlk_mb_az_p32b"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p32b,limit=1] run function rlk:boss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p32b,limit=1] run function rlk:boss/azhdaha/p/meteor/big_hz
