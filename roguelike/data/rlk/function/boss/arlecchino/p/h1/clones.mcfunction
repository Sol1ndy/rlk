# H1 clones (@s = body on the web): two crimson shadow clones left and right of her, each turned toward the lock (yaw
# only), diving in arcs onto the locked spot over 14 t.
execute at @s rotated as @s rotated ~ 0 positioned ^4 ^ ^ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_clone","rlk_kn_clone_l","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:netherite_hoe",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^-4 ^ ^ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_p_h1","rlk_kn_clone","rlk_kn_clone_r","rlk_kn_new"],teleport_duration:1,brightness:{sky:15,block:15},item:{id:"minecraft:netherite_hoe",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_kn_new] positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ ~0.5 ~ run function rlk:mboss/mv/leap {t:14,h:20}
tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
execute at @s run playsound minecraft:entity.illusioner.cast_spell hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
