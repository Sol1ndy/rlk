# 회수/판매 버튼+라벨만 생성 (at = 아이템 위치). macro: price / 참조: #uigid
summon minecraft:interaction ~-0.85 ~0.9 ~ {Tags:["rlk_dbtn","rlk_dbtnR","rlk_duinew","rlk_dgrp"],width:0.82f,height:0.68f,response:true}
summon minecraft:text_display ~-0.85 ~1.05 ~ {Tags:["rlk_dlbl","rlk_dlblR","rlk_duinew","rlk_dgrp"],billboard:"center",see_through:true,background:1073741824,text:{text:"[ 회수 ]",color:"green",bold:true},transformation:{scale:[0.82f,0.82f,0.82f],translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:interaction ~0.85 ~0.9 ~ {Tags:["rlk_dbtn","rlk_dbtnS","rlk_duinew","rlk_dgrp"],width:0.82f,height:0.68f,response:true}
$summon minecraft:text_display ~0.85 ~1.05 ~ {Tags:["rlk_dlbl","rlk_dlblS","rlk_duinew","rlk_dgrp"],billboard:"center",see_through:true,background:1073741824,text:{text:"[ $(price)G에 판매 ]",color:"gold",bold:true},transformation:{scale:[0.82f,0.82f,0.82f],translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rlk_duinew] run scoreboard players operation @s dgid = #uigid tmp
tag @e[tag=rlk_duinew] remove rlk_duinew
