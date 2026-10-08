# 손에 든 활을 당긴 모양으로 (#pm = 0 → 반쯤, 2 → 끝까지). 모양을 바꿀 때마다 손이 한 번 출렁이므로 두 번만 바꾼다
execute if score #pm tmp matches 0 run item modify entity @s hotbar.0 {type:"minecraft:set_components",components:{"minecraft:item_model":"rlk:bow_pull_1"}}
execute if score #pm tmp matches 2 run item modify entity @s hotbar.0 {type:"minecraft:set_components",components:{"minecraft:item_model":"rlk:bow_pull_2"}}
