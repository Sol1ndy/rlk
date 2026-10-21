# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# The Heart in the cradle at the centre: marker rlk_mb_ap_heart (not rlk_mob) + the egg display.
function rlk:boss/apep/heart/clear
summon minecraft:marker 440 201 8 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_heart"]}
summon minecraft:item_display 440 202.2 8 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_heartd"],billboard:"fixed",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f]},item:{id:"minecraft:sniffer_egg",count:1}}
