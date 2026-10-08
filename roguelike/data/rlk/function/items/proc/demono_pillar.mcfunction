# @s = 플레이어, at @s. 지옥의 불기둥: 겹치지 않는 3구역(좌/우/앞뒤)에 각 1개
function rlk:items/proc/demono_dmg
scoreboard players set #elem tmp 1
# 불기둥1: 왼쪽 구역 (x -8~-3)
execute store result storage rlk:dm tx double 0.1 run random value -80..-30
execute store result storage rlk:dm tz double 0.1 run random value -80..80
function rlk:items/proc/demono_pillar2 with storage rlk:dm
# 불기둥2: 오른쪽 구역 (x 3~8)
execute store result storage rlk:dm tx double 0.1 run random value 30..80
execute store result storage rlk:dm tz double 0.1 run random value -80..80
function rlk:items/proc/demono_pillar2 with storage rlk:dm
# 불기둥3: 중앙 앞 또는 뒤 (x -2.5~2.5, z ±4~8)
execute store result storage rlk:dm tx double 0.1 run random value -25..25
execute store result score #pzs tmp run random value 0..1
execute if score #pzs tmp matches 0 store result storage rlk:dm tz double 0.1 run random value 40..80
execute if score #pzs tmp matches 1 store result storage rlk:dm tz double 0.1 run random value -80..-40
function rlk:items/proc/demono_pillar2 with storage rlk:dm
