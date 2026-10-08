$execute unless data storage rlk:pinv order[$(i)] run return run scoreboard players set @s pkSel -1
$data modify storage rlk:io id set from storage rlk:pinv order[$(i)]
function rlk:lvup/ui/item_load with storage rlk:io
execute positioned 105.800 196.550 9.920 run function rlk:lvup/ui/item_big with storage rlk:io
# 판매 가격 = 등급별 가격(rlk:items rarity_price). 보물 각인의 골드 증가는 붙지 않는다
function rlk:ditem/sell_price2 with storage rlk:io
scoreboard players operation #invdPrice tmp = #price tmp
summon minecraft:text_display 107.100 194.100 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_invd_sell","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:[{text:" 판매 ",color:"#FFE08A"},{text:"◆ ",color:"#E0B255"},{score:{name:"#invdPrice",objective:"tmp"},color:"#E0B255"},{text:" "}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 107.100 194.220 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 7
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
