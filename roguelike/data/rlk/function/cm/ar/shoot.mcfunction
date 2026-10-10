# 화살(블록 디스플레이 막대): 0.4칸 × 4 = 1.6칸/틱, 30틱
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_cmp","rlk_cmp_ar","rlk_cmpnew"],teleport_duration:1,block_state:{id:"minecraft:stripped_birch_log"},transformation:{translation:[-0.035f,-0.035f,-0.45f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.07f,0.07f,0.9f]}}
tp @e[tag=rlk_cmpnew] ~ ~ ~ ~ ~
scoreboard players operation @e[tag=rlk_cmpnew] cmD = #cmD_ar tmp
scoreboard players operation @e[tag=rlk_cmpnew] cmLv = #clv tmp
scoreboard players set @e[tag=rlk_cmpnew] cmEl 0
scoreboard players set @e[tag=rlk_cmpnew] cmT 30
tag @e[tag=rlk_cmpnew] remove rlk_cmpnew
kill @s
