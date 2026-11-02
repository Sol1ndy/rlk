# Q2 the flaming wheel (@s = body): a vertical wheel pj from her chest height toward the lock (1.1 b, 1.5 b/t,
# at most 10 t, wall stop, T2 plain Pyro, a new volley group); it bursts on arrival at the lock (tick check),
# at a wall or at the end of its range (pj_end).
function rlk:mboss/grp_new
scoreboard players operation #q2_g kn = #mbGrp mb
scoreboard players set #q2_b kn 0
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.5 positioned ~ 202.2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q2","rlk_kn_wheel","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:fire_charge",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.2f,2.2f,0.2f]}}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet rotated ~ 0 run function rlk:boss/arlecchino/p/q2/launch
