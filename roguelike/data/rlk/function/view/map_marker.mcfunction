# 던전 지도는 room/setup3에서 (0,0)에 만든 축척 0 지도(128x128)다.
# 액자의 북쪽에서 +Z를 보므로 화면 오른쪽은 월드 -X. 실제 몸의 좌표로 표시.
# 지도 픽셀 면과 표식을 같은 깊이에 놓아 FOV에 따른 투영 오차를 없앤다.
# vanilla map_decorations의 영구 표식 누적 없이, 지도 위의 별도 표시만 이동한다.
execute store result score #mapX view run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000
execute store result score #mapZ view run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000
scoreboard players operation #mapX view /= #128 view
scoreboard players operation #mapZ view /= #128 view
scoreboard players set #pinX view 1000004500
scoreboard players set #pinY view 300500
scoreboard players operation #pinX view -= #mapX view
scoreboard players operation #pinY view -= #mapZ view
execute store result storage rlk:map pin.x double 0.001 run scoreboard players get #pinX view
execute store result storage rlk:map pin.y double 0.001 run scoreboard players get #pinY view
execute in minecraft:overworld run function rlk:view/map_marker_place with storage rlk:map pin
