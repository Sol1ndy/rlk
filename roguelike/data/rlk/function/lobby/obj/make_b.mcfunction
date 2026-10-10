# 로비 오브젝트(블록 모양). macro: block name desc color k
$summon minecraft:block_display ~ ~ ~ {Tags:["rlk_lobby","rlk_ldisp","rlk_lnew"],brightness:{sky:15,block:15},block_state:{id:"$(block)"},transformation:{translation:[-0.45f,0.2f,-0.45f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_lobby","rlk_lobj","rlk_lnew"]}
$summon minecraft:text_display ~ ~2.55 ~ {Tags:["rlk_lobby","rlk_llbl","rlk_lk$(k)","rlk_lnew"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,line_width:220,text:[{text:"$(name)",color:"$(color)",bold:true},{text:"\n$(desc)",color:"#D0D0D0",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
summon minecraft:text_display ~ ~2.2 ~ {Tags:["rlk_lobby","rlk_lhint","rlk_lnew"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,0.7f,0.7f]}}
execute store result score #lgid lob run scoreboard players add #lgid lob 1
scoreboard players operation @e[tag=rlk_lnew] lgid = #lgid lob
$scoreboard players set @e[tag=rlk_lnew,tag=rlk_lobj] lact $(k)
tag @e[tag=rlk_lnew] remove rlk_lnew
