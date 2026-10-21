# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# @s = the new nest aux husk, at it: tags, kind, state, the stand-in display (apOI link).
tag @s add rlk_mb_ap_org
tag @s add rlk_mb_ap_nest
scoreboard players set @s apK 4
scoreboard players set @s apS 0
scoreboard players set @s apT 0
scoreboard players add #apOrgN mb 1
scoreboard players operation @s apOI = #apOrgN mb
summon minecraft:item_display ~ ~1.8 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_omnew"],billboard:"vertical",teleport_duration:2,brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f]},item:{id:"minecraft:spore_blossom",count:1}}
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_ap_omnew] apOI = #apOrgN mb
tag @e[type=minecraft:item_display,tag=rlk_mb_ap_omnew] remove rlk_mb_ap_omnew
