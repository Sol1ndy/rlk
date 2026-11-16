# 챕터 보스 문: 아이콘 두 개(나란히) + 이름표 세 줄(텍스트 구성 요소 l1 l2 l3, 그대로 넣음) + 안내 줄. 입력: #oact #oarg tmp,
# 매크로 item/model/item2/model2/l1/l2/l3 (make_node2 와 같은 구조, 이름표만 보스 모듈의 것)
$summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_odisp","rlk_new"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"$(item)",count:1,components:{"minecraft:item_model":"$(model)"}},transformation:{translation:[-0.45f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
$summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_odisp","rlk_new"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"$(item2)",count:1,components:{"minecraft:item_model":"$(model2)"}},transformation:{translation:[0.45f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_room","rlk_obj","rlk_new"]}
$summon minecraft:text_display ~ ~2.55 ~ {Tags:["rlk_room","rlk_olbl","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:[$(l1),{text:"\n"},$(l2),{text:"\n"},$(l3)],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2.2 ~ {Tags:["rlk_room","rlk_ohint","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_new] ogid = #ogid room
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oact = #oact tmp
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oarg = #oarg tmp
tag @e[tag=rlk_new] remove rlk_new
