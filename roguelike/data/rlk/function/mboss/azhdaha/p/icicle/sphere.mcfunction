# The spiky ice sphere over the back (follows the anchor; plan 5 43).
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p43s]
scoreboard players set #aq43L mb 0
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0 ^9 ^2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p43","rlk_mb_az_p43s"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run function rlk:mboss/azhdaha/fx/prop/ice_sphere
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run function rlk:mboss/azhdaha/fx/p/ice_sphere
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run function rlk:mboss/azhdaha/fx/snd/sphere_form
