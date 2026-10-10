# @s = 경험치 지점 표식, at @s. 플레이어가 다가옴 → 샘 생성, 지금 레벨의 필요 경험치만큼 쏟아냄
tag @s remove rlk_xpspot
tag @s add rlk_xpsrc
scoreboard players operation @s xpLeft = @a[tag=player,limit=1] xpNeed
scoreboard players operation @s xpPulse = @s xpLeft
scoreboard players add @s xpPulse 23
scoreboard players operation @s xpPulse /= #c24 tmp
scoreboard players set @s life 0
summon minecraft:block_display ~ ~-1 ~ {Tags:["rlk_room","rlk_odisp"],brightness:{sky:15,block:15},block_state:{id:"minecraft:sculk_catalyst"},transformation:{translation:[-0.5f,1f,-0.5f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}
summon minecraft:text_display ~ ~1.6 ~ {Tags:["rlk_room","rlk_olbl"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:"경험의 샘",color:"#8FD46A",bold:true},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
execute unless score #k19 snd matches 1 run function rlk:snd/f19
execute unless score #k20 snd matches 1 run function rlk:snd/f20
particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.03 20
