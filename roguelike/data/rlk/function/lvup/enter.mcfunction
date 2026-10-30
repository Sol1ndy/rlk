# 선택 공간으로 들어감 (@s = 플레이어, macro: mode = 화면 번호). 노드 화면(7 나무뿌리, 8 인챈트)이 쓴다. 나가기는 lvup/exit
execute if score @s pkMode matches 1.. run return 0
execute if score @s vMap matches 1 run return run function rlk:char/deny {t:"지도를 먼저 닫아 주세요"}
execute if score @s dead matches 1 run return 0
execute in minecraft:overworld unless loaded 104 195 4 run return run function rlk:char/deny {t:"공간을 불러오는 중입니다. 잠시 뒤 다시 시도하세요"}
execute in minecraft:overworld unless block 104 194 4 minecraft:black_concrete run function rlk:lvup/room_build
# 돌아올 자리 기억 (몸 = 1인칭은 플레이어, 숄더뷰는 아바타)
execute store result storage rlk:lvpick ret.x double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result storage rlk:lvpick ret.y double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100
execute store result storage rlk:lvpick ret.z double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute store result storage rlk:lvpick ret.yaw float 0.01 run data get entity @s Rotation[0] 100
execute store result storage rlk:lvpick ret.pitch float 0.01 run data get entity @s Rotation[1] 100
data modify storage rlk:lvpick ret.dim set from entity @s Dimension
execute in minecraft:overworld run tp @s 104.5 195 4.5 0 0
$scoreboard players set @s pkMode $(mode)
scoreboard players set @s pkSel -1
scoreboard players set @s pkConf 0
scoreboard players set @s pkRedraw 2
execute unless score #k71 snd matches 1 run function rlk:snd/f76
