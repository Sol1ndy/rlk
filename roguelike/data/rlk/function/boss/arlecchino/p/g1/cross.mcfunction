# G1 (@s = body): the four giant blades at the ends of the cross through the lock (arms 14 b, the lock marker's
# yaw = the cross axis), the strip decals (t = ticks to the strike in #t kn), the rise burst.
kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~0 0 positioned ^ ^ ^14 positioned ~ 201 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_g1","rlk_kn_blade","rlk_kn_new"],teleport_duration:1}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~90 0 positioned ^ ^ ^14 positioned ~ 201 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_g1","rlk_kn_blade","rlk_kn_new"],teleport_duration:1}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~180 0 positioned ^ ^ ^14 positioned ~ 201 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_g1","rlk_kn_blade","rlk_kn_new"],teleport_duration:1}
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~270 0 positioned ^ ^ ^14 positioned ~ 201 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_g1","rlk_kn_blade","rlk_kn_new"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] run function rlk:boss/arlecchino/fx/prop/blade
tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:boss/arlecchino/fx/snd/blade_rise
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @s run execute positioned ~ ~ ~ run function rlk:boss/arlecchino/fx/p/blade_rise
execute store result storage rlk:kn core.st.yaw int 1 run data get entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] Rotation[0]
execute store result storage rlk:kn core.st.t int 1 run scoreboard players get #t kn
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/strip with storage rlk:kn core.st
execute store result storage rlk:kn core.st.yaw int 1 run scoreboard players get #t2 kn
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/strip with storage rlk:kn core.st
