# 함께 얻는 아이템 미리 보기 (macro: id, 위치 = 아이콘 가운데): 아이콘 + 이름(등급 색 · 별)
$function rlk:lvup/ui/item_load {id:"$(id)"}
function rlk:root/card5 with storage rlk:io
summon minecraft:text_display ~ ~-0.72 ~ {Tags:["rlk_pk","rlk_root_nm"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:150,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f]}}
data modify entity @e[tag=rlk_root_nm,limit=1] text set from storage rlk:io name
tag @e[tag=rlk_root_nm] remove rlk_root_nm
summon minecraft:text_display ~ ~0.32 ~ {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"+ 함께 얻는 아이템",color:"#7CFC9A"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.45f,0.45f,0.45f]}}
