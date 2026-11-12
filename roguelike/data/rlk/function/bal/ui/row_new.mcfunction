# @s = normal / elite enemy, at @s: the pip row (text_display) rides it with the head bar, left end at the bar's left end
execute if score @s balMax matches 4 run summon minecraft:text_display ~ ~ ~ {Tags:["rlk_hb_bal","rlk_bal_new"],billboard:"center",alignment:"center",see_through:true,background:0,shadow:false,text:"",transformation:{translation:[-0.55f,0.02f,0.06f],scale:[0.5f,0.5f,0.5f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
execute if score @s balMax matches 7 run summon minecraft:text_display ~ ~ ~ {Tags:["rlk_hb_bal","rlk_bal_new"],billboard:"center",alignment:"center",see_through:true,background:0,shadow:false,text:"",transformation:{translation:[-0.3625f,0.02f,0.06f],scale:[0.5f,0.5f,0.5f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
ride @e[tag=rlk_bal_new,limit=1] mount @s
tag @e[tag=rlk_bal_new] remove rlk_bal_new
