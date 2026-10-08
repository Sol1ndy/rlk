# 상호작용 오브젝트(아이템 모양). 위치 = 실행 위치(바닥 위). 입력: #oact(동작) #oarg(인자) tmp, 매크로 item/name/desc/color
# 조준(레이)으로 고르고 좌클릭으로 상호작용 — combat/on_attack → room/obj/click
$summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_odisp","rlk_new"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"$(item)",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.3f,1.3f,1.3f]}}
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_room","rlk_obj","rlk_new"]}
$summon minecraft:text_display ~ ~2.55 ~ {Tags:["rlk_room","rlk_olbl","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:[{text:"$(name)",color:"$(color)",bold:true},{text:"\n$(desc)",color:"#D0D0D0",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2.2 ~ {Tags:["rlk_room","rlk_ohint","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_new] ogid = #ogid room
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oact = #oact tmp
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oarg = #oarg tmp
tag @e[tag=rlk_new] remove rlk_new
