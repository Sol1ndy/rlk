# 균열 오브젝트 (위치 = 균열 표식 = 바닥, @s = 그 표식): 조준 표시용 표식(oact 17) + 이름표 "균열" + 안내 줄("▶ 좌클릭",
# room/obj/hover). 좌클릭 → room/obj/click → room/rift/click → room/rift/enter. 균열의 모습(rlk_rift_part)은 이 묶음이
# 아니라서 kill_group 이 지우지 않는다. 열린 균열에만 있다(room/rift/open_now 가 만들고 go · close 가 지움). tools/build_rift.py 가 만듦
scoreboard players operation #riftZid room = @s zid
summon minecraft:marker ~ ~1.45 ~ {Tags:["rlk_room","rlk_obj","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"]}
summon minecraft:text_display ~ ~3.2 ~ {Tags:["rlk_room","rlk_olbl","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:"균열",color:"white",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2.9 ~ {Tags:["rlk_room","rlk_ohint","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_rift_onew] ogid = #ogid room
scoreboard players operation @e[tag=rlk_rift_onew] zid = #riftZid room
scoreboard players set @e[tag=rlk_rift_onew,type=minecraft:marker] oact 17
scoreboard players set @e[tag=rlk_rift_onew,type=minecraft:marker] oarg 0
tag @e[tag=rlk_rift_onew] remove rlk_rift_onew
