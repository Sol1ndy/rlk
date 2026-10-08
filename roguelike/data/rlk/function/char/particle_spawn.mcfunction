$summon minecraft:text_display ~ ~ ~ {Tags:["rlk_epart","rlk_epnew"],billboard:"center",teleport_duration:1,brightness:{sky:15,block:15},background:0,text:{text:"●",color:"$(color)"},transformation:{translation:[0f,-0.1f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]},Rotation:[$(y)f,$(x)f]}
scoreboard players operation @e[tag=rlk_epnew] pcVal = #pcVal tmp
scoreboard players set @e[tag=rlk_epnew] life 0
tag @e[tag=rlk_epnew] remove rlk_epnew
