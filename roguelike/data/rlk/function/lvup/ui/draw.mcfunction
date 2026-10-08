# 선택 공간의 화면을 처음부터 다시 그린다 (@s = 플레이어). 모드: 1 고르는 중, 2 확인 창, 3 바꿀 아이템 고르기
kill @e[tag=rlk_pk]
scoreboard players set @s pkHK 0
scoreboard players set @s pkHI 0
# 인벤토리 상세(모드 4)는 화면이 따로 있다
execute if score @s pkMode matches 4 run return run function rlk:invd/draw
# 아이템 도감(모드 6)도 화면이 따로 있다
execute if score @s pkMode matches 6 run return run function rlk:codex/draw
execute if score @s pkMode matches 1 unless data storage rlk:lvpick choices[0] at @s run function rlk:lvup/roll
scoreboard players operation #pkPend tmp = @s pkPending
summon minecraft:text_display 108.100 199.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"아이템 선택",color:"#FFE08A",bold:true},{text:"  남은 횟수 ",color:"gray",bold:false},{score:{name:"#pkPend",objective:"tmp"},color:"white",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display 103.600 199.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"보유 아이템",color:"white",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display 99.800 199.400 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"각인",color:"white",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display 103.600 193.900 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"Shift + F",color:"#FFE08A"},{text:"  돌아가기 (선택지는 그대로 남습니다)",color:"gray"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
summon minecraft:block_display 104.750 198.450 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 104.750 198.450 9.920 run function rlk:lvup/ui/inv_cell {i:0}
summon minecraft:block_display 103.600 198.450 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 103.600 198.450 9.920 run function rlk:lvup/ui/inv_cell {i:1}
summon minecraft:block_display 102.450 198.450 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 102.450 198.450 9.920 run function rlk:lvup/ui/inv_cell {i:2}
summon minecraft:block_display 104.750 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 104.750 197.300 9.920 run function rlk:lvup/ui/inv_cell {i:3}
summon minecraft:block_display 103.600 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 103.600 197.300 9.920 run function rlk:lvup/ui/inv_cell {i:4}
summon minecraft:block_display 102.450 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 102.450 197.300 9.920 run function rlk:lvup/ui/inv_cell {i:5}
summon minecraft:block_display 104.750 196.150 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 104.750 196.150 9.920 run function rlk:lvup/ui/inv_cell {i:6}
summon minecraft:block_display 103.600 196.150 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 103.600 196.150 9.920 run function rlk:lvup/ui/inv_cell {i:7}
summon minecraft:block_display 102.450 196.150 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 102.450 196.150 9.920 run function rlk:lvup/ui/inv_cell {i:8}
# 현재 캐릭터(조준하면 설명)
summon minecraft:block_display 104.750 194.900 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute positioned 104.750 194.900 9.920 run function rlk:lvup/ui/char_cell
summon minecraft:text_display 103.050 194.650 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"현재 캐릭터\n",color:"gray"},{nbt:"cur.info.name",storage:"rlk:chars",interpret:true,color:"#FFE08A",bold:true}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
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
execute if score @s pkMode matches 1 run function rlk:lvup/ui/draw_browse
execute if score @s pkMode matches 2 run function rlk:lvup/ui/draw_confirm
execute if score @s pkMode matches 3 run function rlk:lvup/ui/draw_swap
execute if score @s pkMode matches 5 run function rlk:lvup/ui/draw_swapconf
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
