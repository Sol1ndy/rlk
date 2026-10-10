# 풀 이슬 표시를 다시 만든다 (@s = 플레이어, 개수가 바뀌었을 때): 칸마다 동그란 테 + 초승달(위에서 아래로)
kill @e[tag=rlk_nfdw]
scoreboard players operation @s nfDwK = @s nfDew
execute if score @s nfDew matches 1.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.70 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"◯",color:"#DDF7C8"},transformation:{translation:[0f,-0.22f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f]}}
execute if score @s nfDew matches 1.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.70 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"☾",color:"#F6FFE8",bold:true},transformation:{translation:[0f,-0.13f,0.01f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players set @e[tag=rlk_nfdw_new] nfDwI 0
tag @e[tag=rlk_nfdw_new] remove rlk_nfdw_new
execute if score @s nfDew matches 2.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.42 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"◯",color:"#DDF7C8"},transformation:{translation:[0f,-0.22f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f]}}
execute if score @s nfDew matches 2.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.42 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"☾",color:"#F6FFE8",bold:true},transformation:{translation:[0f,-0.13f,0.01f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players set @e[tag=rlk_nfdw_new] nfDwI 1
tag @e[tag=rlk_nfdw_new] remove rlk_nfdw_new
execute if score @s nfDew matches 3.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.14 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"◯",color:"#DDF7C8"},transformation:{translation:[0f,-0.22f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.15f,1.15f,1.15f]}}
execute if score @s nfDew matches 3.. at @e[tag=rlk_av,limit=1] run summon minecraft:text_display ~ ~1.14 ~ {Tags:["rlk_nfdw","rlk_nfdw_new"],billboard:"center",teleport_duration:2,background:0,brightness:{sky:15,block:15},shadow:false,alignment:"center",text:{text:"☾",color:"#F6FFE8",bold:true},transformation:{translation:[0f,-0.13f,0.01f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players set @e[tag=rlk_nfdw_new] nfDwI 2
tag @e[tag=rlk_nfdw_new] remove rlk_nfdw_new
execute if score @s nfDew > @s nfDwP unless score #k336 snd matches 1 run function rlk:snd/f396
scoreboard players operation @s nfDwP = @s nfDew
