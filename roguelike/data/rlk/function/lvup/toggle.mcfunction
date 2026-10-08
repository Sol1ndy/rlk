# Shift+F (@s = 플레이어, at @s): 선택 공간으로 들어가거나 돌아온다
execute if score @s pkMode matches 1.. run return run function rlk:lvup/exit
execute unless score @s pkPending matches 1.. run return run function rlk:char/deny {t:"고를 수 있는 아이템이 없습니다 (레벨 업 시 획득)"}
execute if score #active room matches 1 if score #combat room matches 1.. run return run function rlk:char/deny {t:"전투 중에는 이동할 수 없습니다"}
execute in minecraft:overworld unless loaded 104 195 4 run return run function rlk:char/deny {t:"선택 공간을 불러오는 중입니다. 잠시 뒤 다시 시도하세요"}
execute in minecraft:overworld unless block 104 194 4 minecraft:black_concrete run function rlk:lvup/room_build
# 돌아올 자리 기억
execute store result storage rlk:lvpick ret.x double 0.01 run data get entity @s Pos[0] 100
execute store result storage rlk:lvpick ret.y double 0.01 run data get entity @s Pos[1] 100
execute store result storage rlk:lvpick ret.z double 0.01 run data get entity @s Pos[2] 100
execute store result storage rlk:lvpick ret.yaw float 0.01 run data get entity @s Rotation[0] 100
execute store result storage rlk:lvpick ret.pitch float 0.01 run data get entity @s Rotation[1] 100
data modify storage rlk:lvpick ret.dim set from entity @s Dimension
execute in minecraft:overworld run tp @s 104.5 195 4.5 0 0
scoreboard players set @s pkMode 1
scoreboard players set @s pkSel -1
execute unless data storage rlk:lvpick choices[0] run function rlk:lvup/roll
scoreboard players set @s pkRedraw 2
playsound minecraft:block.portal.trigger master @s ~ ~ ~ 0.25 1.8
