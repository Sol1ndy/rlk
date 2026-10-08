# 머리 위 체력바(배경/전경) + 체력 숫자 + 레벨(바 위에 크게) + 상태아이콘 생성 후 몹에 탑승
tag @s add rlk_hb_owner
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_bg","rlk_hb_new"],billboard:"center",brightness:{sky:15,block:15},block_state:{id:"minecraft:black_concrete"},transformation:{translation:[-0.8f,0.25f,0f],scale:[1.6f,0.13f,0.02f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_hb_fg","rlk_hb_new"],billboard:"center",brightness:{sky:15,block:15},block_state:{id:"minecraft:red_concrete"},transformation:{translation:[-0.8f,0.25f,0.01f],scale:[1.6f,0.11f,0.03f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rlk_hb_num","rlk_hb_new"],billboard:"center",alignment:"center",see_through:true,background:0,text:{text:"",color:"white"},transformation:{translation:[0f,0.25f,0.06f],scale:[0.42f,0.42f,0.42f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rlk_hb_lv","rlk_hb_new"],billboard:"center",alignment:"center",see_through:true,background:0,shadow:true,text:{text:""},transformation:{translation:[0f,0.43f,0.06f],scale:[0.95f,0.95f,0.95f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:text_display ~ ~ ~ {Tags:["rlk_hb_icon","rlk_hb_new"],billboard:"center",alignment:"center",see_through:true,background:0,text:{text:"",color:"white"},transformation:{translation:[0f,0.82f,0.06f],scale:[1.4f,1.4f,1.4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[tag=rlk_hb_new] run ride @s mount @e[tag=rlk_hb_owner,limit=1,sort=nearest]
tag @e[tag=rlk_hb_new] remove rlk_hb_new
tag @s remove rlk_hb_owner
