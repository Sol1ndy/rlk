# 아바타가 든 활을 당긴 모양으로 (#pm = 0~2)
execute if score #pm tmp matches 0 run data modify entity @e[tag=rlk_av,limit=1] equipment.mainhand.components."minecraft:item_model" set value "rlk:bow_pull_0"
execute if score #pm tmp matches 1 run data modify entity @e[tag=rlk_av,limit=1] equipment.mainhand.components."minecraft:item_model" set value "rlk:bow_pull_1"
execute if score #pm tmp matches 2 run data modify entity @e[tag=rlk_av,limit=1] equipment.mainhand.components."minecraft:item_model" set value "rlk:bow_pull_2"
