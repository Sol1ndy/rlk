# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# E t70: the Heart is drawn up out of sight (+20 b; idempotent).
execute unless entity @e[tag=rlk_mb_ap_heartd] run summon minecraft:item_display 440 221 8 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_heartd"],billboard:"fixed",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f]},item:{id:"minecraft:sniffer_egg",count:1}}
tp @e[type=minecraft:item_display,tag=rlk_mb_ap_heartd] 440 221 8
