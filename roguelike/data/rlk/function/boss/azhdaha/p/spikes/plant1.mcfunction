# At point 2 (t51): the landing burst and the planted spike.
execute if score #azE mb matches 1 run function rlk:boss/azhdaha/fx/p/impact/1
execute if score #azE mb matches 2 run function rlk:boss/azhdaha/fx/p/impact/2
execute if score #azE mb matches 3 run function rlk:boss/azhdaha/fx/p/impact/3
execute if score #azE mb matches 4 run function rlk:boss/azhdaha/fx/p/impact/4
execute if score #azE mb matches 5 run function rlk:boss/azhdaha/fx/p/impact/5
function rlk:boss/azhdaha/fx/snd/spikes_land
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4s","rlk_mb_az_p4s1","rlk_mb_az_p4n"]}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] run function rlk:boss/azhdaha/fx/prop/spike/5
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] at @s rotated ~57 0 run tp @s ~ ~ ~ ~ 0
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_az_p4n,limit=1] {transformation:{translation:[0f,2.2f,0f],left_rotation:[0.9914f,0f,0f,0.1305f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_mb_az_p4n] remove rlk_mb_az_p4n
