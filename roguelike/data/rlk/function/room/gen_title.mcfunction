$data modify storage rlk:room t set from storage rlk:room types[$(t)]
$scoreboard players set #gtT tmp $(t)
# 노드 맵: 노드 이름("A · B")과 첫 노드 색 (room/node/title)
execute unless score #gtT tmp matches 0 if score #mapType room matches 1..7 run data modify storage rlk:room t set from storage rlk:room nt
# 런 시작 직후(시작 아이템 고르기 중)는 미뤘다가 고르기가 끝날 때(lvup/exit) 띄운다
execute if score #stDefer room matches 1 run return 0
scoreboard players operation #mi tmp = #mapIdx room
scoreboard players add #mi tmp 1
title @s times 8 40 12
scoreboard players set @s ttlT 60
title @s subtitle [{"text":"챕터 ","color":"gray"},{"score":{"name":"#chapter","objective":"room"},"color":"gray"},{"text":"  ·  ","color":"dark_gray"},{"score":{"name":"#mi","objective":"tmp"},"color":"gray"},{"text":" / 6","color":"gray"}]
# 첫 맵(종류 0)은 큰 제목 없이 아래 줄만
execute if score #gtT tmp matches 0 run function rlk:view/ttl_blank
execute unless score #gtT tmp matches 0 run function rlk:room/gen_title2 with storage rlk:room t
execute at @s unless score #k4 snd matches 1 run function rlk:snd/f4
