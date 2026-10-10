scoreboard players operation @s cmShM = @s mhpM
scoreboard players operation @s cmShM *= #cmShPct tmp
scoreboard players operation @s cmShM /= #100 tmp
execute if score @s cmShM matches ..0 run scoreboard players set @s cmShM 1
scoreboard players operation @s cmSh = @s cmShM
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_cmlink","rlk_cmshbar","rlk_cmnew2"],billboard:"center",brightness:{sky:15,block:15},block_state:{id:"minecraft:light_blue_concrete"},transformation:{translation:[-0.8f,0.15f,0.015f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,0.07f,0.03f]}}
scoreboard players operation @e[tag=rlk_cmnew2] cmId = #cid tmp
ride @e[tag=rlk_cmnew2,limit=1] mount @s
tag @e[tag=rlk_cmnew2] remove rlk_cmnew2
