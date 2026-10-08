# @s = 플레이어, at @s. 심연의 촉수: 주변(8) 임의 위치에서 촉수가 솟아 그 주변 타격
function rlk:items/proc/demono_dmg
scoreboard players set #elem tmp 2
execute store result storage rlk:dm tx double 0.1 run random value -70..70
execute store result storage rlk:dm tz double 0.1 run random value -70..70
function rlk:items/proc/demono_tentacle2 with storage rlk:dm
