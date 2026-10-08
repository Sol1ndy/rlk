# 인벤이 가득 참: 고른 아이템과 바꿀 인벤 아이템을 고른다
summon minecraft:block_display 108.100 198.100 9.970 {Tags:["rlk_pk"],brightness:{sky:15,block:15},block_state:{id:"minecraft:gray_concrete"},transformation:{translation:[-0.750f,-0.750f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.500f,1.500f,0.02f]}}
execute positioned 108.100 198.100 9.920 run function rlk:lvup/ui/selected
summon minecraft:text_display 108.100 196.000 9.920 {Tags:["rlk_pk"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:0,line_width:400,text:[{text:"인벤토리가 가득 찼습니다\n",color:"#E06A5A"},{text:"바꿀 아이템을 오른쪽에서 고르세요\n(내려놓은 아이템은 돌아가면 발밑에 놓입니다)",color:"white"}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:text_display 108.100 195.300 9.920 {Tags:["rlk_pk","rlk_pk_d","rlk_pk_new"],Rotation:[180f,0f],brightness:{sky:15,block:15},alignment:"center",background:1344282672,line_width:400,text:{text:" 취소 ",color:"#E06A5A"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker 108.100 195.420 9.920 {Tags:["rlk_pk","rlk_pk_el","rlk_pk_new"]}
scoreboard players set @e[tag=rlk_pk_new] pkKind 6
scoreboard players set @e[tag=rlk_pk_new] pkIdx 0
tag @e[tag=rlk_pk_new] remove rlk_pk_new
