# 아이템 설명(정보) 패널만 생성 (at = 아이템 위치). 참조: rlk:dui name, #uigid
summon minecraft:text_display ~ ~1.9 ~ {Tags:["rlk_dinfo","rlk_duinew2","rlk_dgrp"],billboard:"vertical",see_through:true,alignment:"center",line_width:200,background:1073741824,text:{text:""},transformation:{scale:[0.9f,0.9f,0.9f],translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rlk_duinew2] run scoreboard players operation @s dgid = #uigid tmp
data modify entity @e[tag=rlk_dinfo,tag=rlk_duinew2,limit=1] text set from storage rlk:dui name
tag @e[tag=rlk_duinew2] remove rlk_duinew2
