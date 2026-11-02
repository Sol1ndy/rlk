# The outward crescent turns back (@s = it): a new returning crescent here, flying toward her for as many ticks
# as the outward leg flew, in the same volley group (one landing per throw), no wall stop.
execute store result storage rlk:kn p2.cr.life int 1 run scoreboard players get @s mbPjT
execute store result storage rlk:kn p2.cr.g int 1 run scoreboard players get @s mbPjG
execute store result storage rlk:kn p2.cr.kb int 1 run scoreboard players get @s mbPjB
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_q3","rlk_kn_cres","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:netherite_hoe",count:1},transformation:{left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.8f,1.8f,1.8f]}}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run function rlk:boss/arlecchino/p/q3/cres_back with storage rlk:kn p2.cr
