# 고르는 중: 선택지(개수에 따라 삼각형/사각형/오각형) + 리롤 + 넘기기
execute store result score #pkN tmp run data get storage rlk:lvpick choices
execute if score #pkN tmp matches 0 run summon minecraft:text_display 108.100 197.300 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"고를 수 있는 아이템이 없습니다",color:"gray"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute if score #pkN tmp matches 1 run summon minecraft:block_display 108.100 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 1 positioned 108.100 197.300 9.920 run function rlk:lvup/ui/choice {i:0}
execute if score #pkN tmp matches 2 run summon minecraft:block_display 109.050 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 2 positioned 109.050 197.300 9.920 run function rlk:lvup/ui/choice {i:0}
execute if score #pkN tmp matches 2 run summon minecraft:block_display 107.150 197.300 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 2 positioned 107.150 197.300 9.920 run function rlk:lvup/ui/choice {i:1}
execute if score #pkN tmp matches 3 run summon minecraft:block_display 108.100 198.650 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 3 positioned 108.100 198.650 9.920 run function rlk:lvup/ui/choice {i:0}
execute if score #pkN tmp matches 3 run summon minecraft:block_display 106.931 196.625 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 3 positioned 106.931 196.625 9.920 run function rlk:lvup/ui/choice {i:1}
execute if score #pkN tmp matches 3 run summon minecraft:block_display 109.269 196.625 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 3 positioned 109.269 196.625 9.920 run function rlk:lvup/ui/choice {i:2}
execute if score #pkN tmp matches 4 run summon minecraft:block_display 109.055 198.255 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 4 positioned 109.055 198.255 9.920 run function rlk:lvup/ui/choice {i:0}
execute if score #pkN tmp matches 4 run summon minecraft:block_display 107.145 198.255 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 4 positioned 107.145 198.255 9.920 run function rlk:lvup/ui/choice {i:1}
execute if score #pkN tmp matches 4 run summon minecraft:block_display 107.145 196.345 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 4 positioned 107.145 196.345 9.920 run function rlk:lvup/ui/choice {i:2}
execute if score #pkN tmp matches 4 run summon minecraft:block_display 109.055 196.345 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 4 positioned 109.055 196.345 9.920 run function rlk:lvup/ui/choice {i:3}
execute if score #pkN tmp matches 5 run summon minecraft:block_display 108.100 198.650 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 5 positioned 108.100 198.650 9.920 run function rlk:lvup/ui/choice {i:0}
execute if score #pkN tmp matches 5 run summon minecraft:block_display 106.816 197.717 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 5 positioned 106.816 197.717 9.920 run function rlk:lvup/ui/choice {i:1}
execute if score #pkN tmp matches 5 run summon minecraft:block_display 107.306 196.208 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 5 positioned 107.306 196.208 9.920 run function rlk:lvup/ui/choice {i:2}
execute if score #pkN tmp matches 5 run summon minecraft:block_display 108.894 196.208 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 5 positioned 108.894 196.208 9.920 run function rlk:lvup/ui/choice {i:3}
execute if score #pkN tmp matches 5 run summon minecraft:block_display 109.384 197.717 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.500f,-0.500f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.000f,1.000f,0.02f]}}
execute if score #pkN tmp matches 5 positioned 109.384 197.717 9.920 run function rlk:lvup/ui/choice {i:4}
summon minecraft:text_display 109.100 194.900 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 리롤 ",color:"#FFE08A"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 109.100 195.020 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 3
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
function rlk:lvup/rr_cost
scoreboard players operation #pkDice tmp = @s dice
execute unless score #pkDice tmp matches 0.. run scoreboard players set #pkDice tmp 0
execute if score #pkRerollCost tmp matches 1.. run summon minecraft:text_display 109.100 194.500 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"⚄ ",color:"#F2F2F2"},{score:{name:"#pkRerollCost",objective:"tmp"},color:"#F2F2F2"},{text:"  (보유 ",color:"gray"},{score:{name:"#pkDice",objective:"tmp"},color:"gray"},{text:")",color:"gray"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
execute if score #pkRerollCost tmp matches ..0 run summon minecraft:text_display 109.100 194.500 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:{text:"무료",color:"#8FD46A",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
summon minecraft:text_display 107.100 194.900 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 넘기기 ",color:"#C9C9C9"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 107.100 195.020 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 4
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
