# 다른 화면의 복귀 좌표가 지도 방으로 저장되지 않게 한다.
execute if score @s vMap matches 1 run return run function rlk:char/deny {t:"지도를 먼저 닫아 주세요"}
# @s = 플레이어, at @s. 도감 안이면 돌아가고, 아니면 선택 공간과 같은 방으로 이동해 도감(모드 6)을 연다
execute if score @s pkMode matches 6 run return run function rlk:lvup/exit
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute if score #active room matches 1 if score #combat room matches 1.. run return run function rlk:char/deny {t:"전투 중에는 이동할 수 없습니다"}
execute in minecraft:overworld unless loaded 104 195 4 run return run function rlk:char/deny {t:"공간을 불러오는 중입니다. 잠시 뒤 다시 시도하세요"}
execute in minecraft:overworld unless block 104 194 4 minecraft:black_concrete run function rlk:lvup/room_build
execute store result storage rlk:lvpick ret.x double 0.01 run data get entity @s Pos[0] 100
execute store result storage rlk:lvpick ret.y double 0.01 run data get entity @s Pos[1] 100
execute store result storage rlk:lvpick ret.z double 0.01 run data get entity @s Pos[2] 100
execute store result storage rlk:lvpick ret.yaw float 0.01 run data get entity @s Rotation[0] 100
execute store result storage rlk:lvpick ret.pitch float 0.01 run data get entity @s Rotation[1] 100
data modify storage rlk:lvpick ret.dim set from entity @s Dimension
execute in minecraft:overworld run tp @s 104.5 195 4.5 0 0
function rlk:codex/labels
function rlk:codex/lists
scoreboard players set @s pkMode 6
scoreboard players set @s pkSel -1
scoreboard players set @s pkConf 0
scoreboard players set @s cxTab 0
scoreboard players set @s cxPage 0
scoreboard players set @s pkRedraw 2
execute unless score #k71 snd matches 1 run function rlk:snd/f76
