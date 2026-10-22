# 인챈트 화면 (pkMode 8, @s = 플레이어, lvup/ui/draw 에서): 보유 아이템 18칸(9칸씩 두 줄, 인벤토리와 같은 순서) + 돌아가기
summon minecraft:text_display 105.800 199.650 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"인챈트",color:"#B58BE8",bold:true},{text:"   남은 강화 ",color:"gray",bold:false},{score:{name:"#enchN",objective:"room"},color:"#FFE08A",bold:true}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
summon minecraft:text_display 105.800 198.850 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"아이템을 누를 때마다 별이 하나 오릅니다 (최대 ★★★)\n같은 아이템을 여러 번 골라도 됩니다",color:"#D8D8D8"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute positioned 109.600 198.250 9.920 run function rlk:ench/cell {i:0}
execute positioned 108.650 198.250 9.920 run function rlk:ench/cell {i:1}
execute positioned 107.700 198.250 9.920 run function rlk:ench/cell {i:2}
execute positioned 106.750 198.250 9.920 run function rlk:ench/cell {i:3}
execute positioned 105.800 198.250 9.920 run function rlk:ench/cell {i:4}
execute positioned 104.850 198.250 9.920 run function rlk:ench/cell {i:5}
execute positioned 103.900 198.250 9.920 run function rlk:ench/cell {i:6}
execute positioned 102.950 198.250 9.920 run function rlk:ench/cell {i:7}
execute positioned 102.000 198.250 9.920 run function rlk:ench/cell {i:8}
execute positioned 109.600 197.050 9.920 run function rlk:ench/cell {i:9}
execute positioned 108.650 197.050 9.920 run function rlk:ench/cell {i:10}
execute positioned 107.700 197.050 9.920 run function rlk:ench/cell {i:11}
execute positioned 106.750 197.050 9.920 run function rlk:ench/cell {i:12}
execute positioned 105.800 197.050 9.920 run function rlk:ench/cell {i:13}
execute positioned 104.850 197.050 9.920 run function rlk:ench/cell {i:14}
execute positioned 103.900 197.050 9.920 run function rlk:ench/cell {i:15}
execute positioned 102.950 197.050 9.920 run function rlk:ench/cell {i:16}
execute positioned 102.000 197.050 9.920 run function rlk:ench/cell {i:17}
summon minecraft:text_display 105.800 194.400 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 돌아가기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 105.800 194.520 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 8
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 105.800 193.700 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"남은 횟수는 돌아가도 인챈트대에 그대로 남습니다",color:"#B0B0B0"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
