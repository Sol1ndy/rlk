# 상호작용 오브젝트(블록 모양). 입력은 make_item 과 같고 item 대신 block
$summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_odisp","rlk_new"],brightness:{sky:15,block:15},block_state:{id:"$(block)"},transformation:{translation:[-0.6f,0f,-0.6f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_room","rlk_obj","rlk_new"]}
$summon minecraft:text_display ~ ~2.55 ~ {Tags:["rlk_room","rlk_olbl","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:[{text:"$(name)",color:"$(color)",bold:true},{text:"\n$(desc)",color:"#D0D0D0",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2.2 ~ {Tags:["rlk_room","rlk_ohint","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_new] ogid = #ogid room
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oact = #oact tmp
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oarg = #oarg tmp
tag @e[tag=rlk_new] remove rlk_new
