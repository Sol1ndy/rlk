# 나무뿌리 화면 (pkMode 7, @s = 플레이어, lvup/ui/draw 에서): 각인 카드 셋(종류 14) + 돌아가기(종류 8)
summon minecraft:text_display 105.800 199.500 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"세계수의 나무뿌리",color:"#B08A5A",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
summon minecraft:text_display 105.800 198.700 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"각인 하나를 골라 ",color:"#D8D8D8"},{text:"기적",color:"#7CFC9A"},{text:"을 받습니다 (한 판에 한 번)\n그 각인이 달린 아이템도 하나 얻습니다",color:"#D8D8D8"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute positioned 108.300 196.900 9.920 run function rlk:root/card {i:0}
execute positioned 105.800 196.900 9.920 run function rlk:root/card {i:1}
execute positioned 103.300 196.900 9.920 run function rlk:root/card {i:2}
summon minecraft:text_display 105.800 194.100 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 돌아가기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 105.800 194.220 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 8
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 105.800 193.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"고르지 않고 돌아가면 나무뿌리는 그대로 남습니다",color:"#B0B0B0"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
