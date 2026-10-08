$summon minecraft:item_display ~ ~ ~ {Tags:["rlk_pk","rlk_pk_big"],Rotation:[180f,0f],brightness:{sky:15,block:15},item_display:"gui",item:{id:"$(item)",count:1,components:{"minecraft:item_model":"$(model)"}},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
$summon minecraft:text_display ~ ~-1.15 ~ {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:$(name),transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
execute if data storage rlk:io src.prof run data modify entity @e[tag=rlk_pk_big,limit=1] item.components."minecraft:profile" set from storage rlk:io src.prof
# 머리는 얼굴이 정면을 보게
execute if data storage rlk:io src.prof run data modify entity @e[tag=rlk_pk_big,limit=1] item_display set value "fixed"
tag @e[tag=rlk_pk_big] remove rlk_pk_big
