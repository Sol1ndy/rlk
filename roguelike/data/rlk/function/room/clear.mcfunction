# 현재 맵 치우기 (오버월드에서 실행): 지은 구역·문 블록 제거 + 방 엔티티 제거
execute as @e[tag=rlk_zone,scores={zst=1..}] run function rlk:room/zone_erase
execute as @e[tag=rlk_door,scores={dst=1..}] run function rlk:room/door_erase with entity @s data
kill @e[tag=rlk_room]
execute positioned -64 180 -64 run kill @e[type=minecraft:arrow,dx=127,dy=40,dz=127]
execute positioned -64 180 -64 run kill @e[type=minecraft:item,dx=127,dy=17,dz=127]
execute positioned -64 198 -64 run kill @e[type=minecraft:experience_orb,dx=127,dy=20,dz=127]
execute positioned -64 198 -64 run kill @e[tag=rlk_healorb,dx=127,dy=20,dz=127]
scoreboard players set #combat room 0
scoreboard players set #spawnT room 0
scoreboard players set #seal room 0
