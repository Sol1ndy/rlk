# 누를 수 있는 아이템 표시 + 이름표(선택지만. 보유 아이템은 칸이 붙어 있어 이름을 설명 창에서만 보여 줌) + 요소 표식. 종류/번호는 #pkKind / #pkIdx
$summon minecraft:item_display ~ ~ ~ {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},item_display:"gui",glow_color_override:16768138,item:{id:"$(item)",count:1,components:{"minecraft:item_model":"$(model)"}},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f]}}
$execute if score #pkKind tmp matches 1 run summon minecraft:text_display ~ ~-1.02 ~ {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:68,text:{text:"$(nm)",color:"$(color)"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
execute if data storage rlk:io src.prof run data modify entity @e[tag=rlk_pk_new,type=minecraft:item_display,limit=1] item.components."minecraft:profile" set from storage rlk:io src.prof
# 머리는 얼굴이 정면을 보게
execute if data storage rlk:io src.prof run data modify entity @e[tag=rlk_pk_new,type=minecraft:item_display,limit=1] item_display set value "fixed"
summon minecraft:marker ~ ~ ~ {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players operation @e[tag=rlk_pk_new] pkKind = #pkKind tmp
scoreboard players operation @e[tag=rlk_pk_new] pkIdx = #pkIdx tmp
tag @e[tag=rlk_pk_new] remove rlk_pk_new
