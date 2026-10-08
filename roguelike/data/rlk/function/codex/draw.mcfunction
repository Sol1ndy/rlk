# 도감 화면 (@s = 플레이어, lvup/ui/draw 에서 pkMode 6 일 때)
# 지금 탭의 목록 → rlk:codex list
execute if score @s cxTab matches 0 run data modify storage rlk:codex list set from storage rlk:codex byrar.common
execute if score @s cxTab matches 1 run data modify storage rlk:codex list set from storage rlk:codex byrar.rare
execute if score @s cxTab matches 2 run data modify storage rlk:codex list set from storage rlk:codex byrar.epic
execute if score @s cxTab matches 3 run data modify storage rlk:codex list set from storage rlk:codex byrar.legendary
execute if score @s cxTab matches 4 run data modify storage rlk:codex list set from storage rlk:codex byrar.mythic
execute if score @s cxTab matches 5 run data modify storage rlk:codex list set from storage rlk:codex chars
execute store result score #cxN tmp run data get storage rlk:codex list
# 쪽 수 = (개수 + 23) / 24, 지금 쪽이 범위를 벗어나면 맞춘다
scoreboard players operation #cxPg tmp = #cxN tmp
scoreboard players add #cxPg tmp 23
scoreboard players operation #cxPg tmp /= #c24 tmp
execute if score #cxPg tmp matches ..0 run scoreboard players set #cxPg tmp 1
execute if score @s cxPage >= #cxPg tmp run scoreboard players set @s cxPage 0
execute if score @s cxPage matches ..-1 run scoreboard players set @s cxPage 0
scoreboard players operation #cxCur tmp = @s cxPage
scoreboard players add #cxCur tmp 1
execute unless score @s cxMode matches 1 run summon minecraft:text_display 104.325 199.650 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"아이템 도감",color:"#FFE08A",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
execute if score @s cxMode matches 1 run summon minecraft:text_display 104.325 199.650 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"시작 아이템 고르기  ",color:"#FFE08A",bold:true},{text:"남은 선택 ",color:"gray",bold:false},{score:{name:"#stPick",objective:"room"},color:"white",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}
execute unless score @s cxMode matches 1 run summon minecraft:text_display 104.325 199.250 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"조준 = 설명  ·  좌클릭 = 인벤토리에 바로 추가 (캐릭터는 교체)  ·  ",color:"gray"},{score:{name:"#cxN",objective:"tmp"},color:"white"},{text:"개",color:"gray"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f]}}
execute if score @s cxMode matches 1 run summon minecraft:text_display 104.325 199.250 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"조준 = 설명  ·  좌클릭 = 이 아이템을 가지고 시작",color:"gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f]}}
execute if score @s cxTab matches 0 run summon minecraft:text_display 107.525 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" COMMON ",color:"green",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxTab matches 0 run summon minecraft:text_display 107.525 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" COMMON ",color:"green"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
summon minecraft:marker 107.525 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute if score @s cxTab matches 1 run summon minecraft:text_display 106.245 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" RARE ",color:"aqua",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxTab matches 1 run summon minecraft:text_display 106.245 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" RARE ",color:"aqua"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
summon minecraft:marker 106.245 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 1
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute unless score @s cxMode matches 1 run execute if score @s cxTab matches 2 run summon minecraft:text_display 104.965 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" UNIQUE ",color:"dark_purple",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run execute unless score @s cxTab matches 2 run summon minecraft:text_display 104.965 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" UNIQUE ",color:"dark_purple"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run summon minecraft:marker 104.965 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 2
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute unless score @s cxMode matches 1 run execute if score @s cxTab matches 3 run summon minecraft:text_display 103.525 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" LEGENDARY ",color:"yellow",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run execute unless score @s cxTab matches 3 run summon minecraft:text_display 103.525 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" LEGENDARY ",color:"yellow"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run summon minecraft:marker 103.525 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 3
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute unless score @s cxMode matches 1 run execute if score @s cxTab matches 4 run summon minecraft:text_display 102.025 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" MYTHIC ",color:"dark_red",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run execute unless score @s cxTab matches 4 run summon minecraft:text_display 102.025 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" MYTHIC ",color:"dark_red"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run summon minecraft:marker 102.025 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 4
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute unless score @s cxMode matches 1 run execute if score @s cxTab matches 5 run summon minecraft:text_display 100.725 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 캐릭터 ",color:"gold",bold:true,underlined:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run execute unless score @s cxTab matches 5 run summon minecraft:text_display 100.725 198.620 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 캐릭터 ",color:"gold"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute unless score @s cxMode matches 1 run summon minecraft:marker 100.725 198.740 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 10
scoreboard players set @e[tag=rlk_pk_new] pkIdx 5
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute positioned 107.825 197.500 9.920 run function rlk:codex/cell {i:0}
execute positioned 106.875 197.500 9.920 run function rlk:codex/cell {i:1}
execute positioned 105.925 197.500 9.920 run function rlk:codex/cell {i:2}
execute positioned 104.975 197.500 9.920 run function rlk:codex/cell {i:3}
execute positioned 104.025 197.500 9.920 run function rlk:codex/cell {i:4}
execute positioned 103.075 197.500 9.920 run function rlk:codex/cell {i:5}
execute positioned 102.125 197.500 9.920 run function rlk:codex/cell {i:6}
execute positioned 101.175 197.500 9.920 run function rlk:codex/cell {i:7}
execute positioned 107.825 196.120 9.920 run function rlk:codex/cell {i:8}
execute positioned 106.875 196.120 9.920 run function rlk:codex/cell {i:9}
execute positioned 105.925 196.120 9.920 run function rlk:codex/cell {i:10}
execute positioned 104.975 196.120 9.920 run function rlk:codex/cell {i:11}
execute positioned 104.025 196.120 9.920 run function rlk:codex/cell {i:12}
execute positioned 103.075 196.120 9.920 run function rlk:codex/cell {i:13}
execute positioned 102.125 196.120 9.920 run function rlk:codex/cell {i:14}
execute positioned 101.175 196.120 9.920 run function rlk:codex/cell {i:15}
execute positioned 107.825 194.740 9.920 run function rlk:codex/cell {i:16}
execute positioned 106.875 194.740 9.920 run function rlk:codex/cell {i:17}
execute positioned 105.925 194.740 9.920 run function rlk:codex/cell {i:18}
execute positioned 104.975 194.740 9.920 run function rlk:codex/cell {i:19}
execute positioned 104.025 194.740 9.920 run function rlk:codex/cell {i:20}
execute positioned 103.075 194.740 9.920 run function rlk:codex/cell {i:21}
execute positioned 102.125 194.740 9.920 run function rlk:codex/cell {i:22}
execute positioned 101.175 194.740 9.920 run function rlk:codex/cell {i:23}
summon minecraft:text_display 105.825 193.450 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" ◀ 이전 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:marker 105.825 193.570 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 11
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 104.325 193.450 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{score:{name:"#cxCur",objective:"tmp"},color:"white"},{text:" / ",color:"gray"},{score:{name:"#cxPg",objective:"tmp"},color:"white"},{text:" 쪽",color:"gray"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:text_display 102.825 193.450 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 다음 ▶ ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:marker 102.825 193.570 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 12
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
execute unless score @s cxMode matches 1 run summon minecraft:text_display 100.425 193.450 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 돌아가기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute if score @s cxMode matches 1 run summon minecraft:text_display 100.425 193.450 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 건너뛰기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:marker 100.425 193.570 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 8
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
summon minecraft:text_display 104.500 196.600 6.500 {Tags:["rlk_pk","rlk_pk_tip2"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},alignment:"left",line_width:230,background:-535752688,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
