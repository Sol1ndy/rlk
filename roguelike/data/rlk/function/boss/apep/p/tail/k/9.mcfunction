# tail #apPT 9
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p5f]
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p5","rlk_mb_ap_p5f"]}
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p5f,limit=1] ~ ~ ~ ~ 0
