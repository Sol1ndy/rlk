# 중간보스 아이템 상자 오브젝트 (위치 = 상자 바닥 가운데). mboss/box/land 가 상자가 땅에 닿는 틱에 부른다.
# 좌클릭(oact 15 → room/obj/do_mbox)하면 챕터 등급 아이템 선택 1번. 상자 모양(떨어진 item_display, 크기 1.1 = 높이 약 0.96칸)은
# 부르기 전에 rlk_new 를 붙여 두어 같은 묶음(ogid)이 된다 → kill_group 이 그 상자만 지운다.
# 두 상자가 1.5칸 간격으로 나란히 서므로 글자를 조금 작게(0.8) 하고 설명을 두 줄로 나눈다(옆 상자 글자와 겹치지 않게)
scoreboard players set #oact tmp 15
scoreboard players set #oarg tmp 0
summon minecraft:marker ~ ~0.55 ~ {Tags:["rlk_room","rlk_obj","rlk_new"]}
summon minecraft:text_display ~ ~1.4 ~ {Tags:["rlk_room","rlk_olbl","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:[{text:"아이템 상자",color:"#FFD24A",bold:true},{text:"\n챕터 등급\n아이템 선택",color:"#D0D0D0",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
summon minecraft:text_display ~ ~1.08 ~ {Tags:["rlk_room","rlk_ohint","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_new] ogid = #ogid room
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oact = #oact tmp
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oarg = #oarg tmp
tag @e[tag=rlk_new] remove rlk_new
