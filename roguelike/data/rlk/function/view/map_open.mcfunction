# @s = 플레이어. 모험 모드의 고정 지도 화면: 클릭 이벤트를 계속 받을 수 있다.
execute if score @s vMap matches 1 run return 0
execute if score @s dead matches 1 run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
execute unless score #active room matches 1 run return run function rlk:char/deny {t:"지도는 던전에서 사용할 수 있습니다"}
execute if score #combat room matches 1.. run return run function rlk:char/deny {t:"전투 중에는 지도를 볼 수 없습니다"}
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute in minecraft:overworld unless loaded 1000004 300 1000004 run return run function rlk:char/deny {t:"지도를 불러오는 중입니다"}
execute in minecraft:overworld unless data storage rlk:map {version:3} run function rlk:view/map_room
execute in minecraft:overworld unless entity @e[tag=rlk_mapframe,limit=1] run function rlk:view/map_room
execute in minecraft:overworld unless entity @e[tag=rlk_mappin,limit=1] run function rlk:view/map_room
execute unless data storage rlk:room map_id run return run function rlk:char/deny {t:"지도를 불러오는 중입니다"}
execute in minecraft:overworld run function rlk:room/map_frame with storage rlk:room
execute in minecraft:overworld run item modify entity @e[tag=rlk_mapframe,limit=1] contents {type:"minecraft:set_components",components:{"minecraft:item_model":"minecraft:filled_map"}}
# 위치/시선/속성은 한 명용 저장소에 정확히 저장한다. 1인칭도 같은 화면을 사용한다.
data modify storage rlk:map ret set value {scale:1d,camera:4d,gravity:0.08d,was_body:0b}
data modify storage rlk:map ret.x set from entity @e[tag=rlk_body,limit=1] Pos[0]
data modify storage rlk:map ret.y set from entity @e[tag=rlk_body,limit=1] Pos[1]
data modify storage rlk:map ret.z set from entity @e[tag=rlk_body,limit=1] Pos[2]
data modify storage rlk:map ret.yaw set from entity @s Rotation[0]
data modify storage rlk:map ret.pitch set from entity @s Rotation[1]
data modify storage rlk:map ret.dim set from entity @s Dimension
execute store result storage rlk:map ret.scale double 0.0001 run attribute @s minecraft:scale base get 10000
execute store result storage rlk:map ret.camera double 0.0001 run attribute @s minecraft:camera_distance base get 10000
execute store result storage rlk:map ret.gravity double 0.0001 run attribute @s minecraft:gravity base get 10000
execute if entity @s[tag=rlk_body] run data modify storage rlk:map ret.was_body set value 1b
kill @e[tag=rlk_mapreturn]
execute if entity @s[tag=rlk_body] at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mapreturn","rlk_body"]}
tag @s remove rlk_body
tag @s remove rlk_mgS
tag @s remove rlk_mgA
tag @s remove rlk_mgC
execute if entity @s[gamemode=survival] run tag @s add rlk_mgS
execute if entity @s[gamemode=adventure] run tag @s add rlk_mgA
execute if entity @s[gamemode=creative] run tag @s add rlk_mgC
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
ride @s dismount
gamemode adventure @s
attribute @s minecraft:scale base set 0.0625
attribute @s minecraft:camera_distance base set 0
attribute @s minecraft:gravity base set 0
scoreboard players set @s vMap 1
scoreboard players set @s vMapT 0
scoreboard players set @s vMapH 8
function rlk:view/map_position
function rlk:view/map_marker
title @s clear
title @s actionbar {text:"지도 · 좌클릭 / 우클릭으로 닫기",color:"gold"}
execute unless score #k205 snd matches 1 run function rlk:snd/f225
