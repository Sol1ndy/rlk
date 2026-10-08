# 인벤토리 상세 화면 (@s = 플레이어, lvup/ui/draw 에서 pkMode 4 일 때). 보유 아이템 9칸을 한 줄로(인벤토리 둘째 줄과 같은 순서)
scoreboard players set @s pkConf 0
summon minecraft:text_display 105.800 199.650 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"인벤토리 상세",color:"#FFE08A",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
summon minecraft:text_display 105.800 198.850 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"아이템을 누른 뒤 다른 아이템을 누르면\n두 아이템의 자리가 바뀝니다",color:"#D8D8D8"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.85f,0.85f,0.85f]}}
summon minecraft:text_display 99.800 199.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"각인",color:"white",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
execute positioned 109.600 198.000 9.920 run function rlk:invd/cell {i:0}
summon minecraft:text_display 109.600 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"1",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 108.650 198.000 9.920 run function rlk:invd/cell {i:1}
summon minecraft:text_display 108.650 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"2",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 107.700 198.000 9.920 run function rlk:invd/cell {i:2}
summon minecraft:text_display 107.700 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"3",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 106.750 198.000 9.920 run function rlk:invd/cell {i:3}
summon minecraft:text_display 106.750 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"4",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 105.800 198.000 9.920 run function rlk:invd/cell {i:4}
summon minecraft:text_display 105.800 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"5",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 104.850 198.000 9.920 run function rlk:invd/cell {i:5}
summon minecraft:text_display 104.850 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"6",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 103.900 198.000 9.920 run function rlk:invd/cell {i:6}
summon minecraft:text_display 103.900 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"7",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 102.950 198.000 9.920 run function rlk:invd/cell {i:7}
summon minecraft:text_display 102.950 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"8",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
execute positioned 102.000 198.000 9.920 run function rlk:invd/cell {i:8}
summon minecraft:text_display 102.000 197.280 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"9",color:"dark_gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
summon minecraft:text_display 99.800 198.750 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 198.290 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 1
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 197.830 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 2
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 197.370 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 3
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 196.910 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 4
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 196.450 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 5
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 195.990 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 6
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 195.530 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 7
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 195.070 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 8
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 194.610 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 9
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 194.150 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 10
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 193.690 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 11
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 193.230 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 12
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 192.770 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 13
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip2"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
execute unless data storage rlk:pinv order[0] run summon minecraft:text_display 105.800 196.300 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"가진 아이템이 없습니다",color:"gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute if data storage rlk:pinv order[0] if score @s pkSel matches -1 run summon minecraft:text_display 105.800 196.300 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"자리를 바꾸거나 팔 아이템을 고르세요",color:"gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute if score @s pkSel matches 0.. run function rlk:invd/draw_sel
summon minecraft:text_display 104.500 194.100 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 돌아가기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 104.500 194.220 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 8
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 105.800 193.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"Shift + F",color:"#FFE08A"},{text:"  또는 인벤토리의 버튼을 다시 눌러도 돌아갑니다",color:"#B0B0B0"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
summon minecraft:text_display 99.800 192.310 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 14
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 191.850 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 15
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 191.390 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 16
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 99.800 190.930 9.920 {Tags:["rlk_pk","rlk_pk_er","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
scoreboard players set @e[tag=rlk_pk_new] pkIdx 17
tag @e[tag=rlk_pk_new] remove rlk_pk_new
function rlk:lvup/eng/refresh
