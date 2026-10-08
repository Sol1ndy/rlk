# 밤 꿰뚫기: 생명의 계약을 해소하고 그 #clHeal%(100% 이상이었으면 #clHeal2%)만큼 회복 (@s = 플레이어, #clB = 찌르기 전 생명의 계약 %)
function rlk:player/bol/clear
scoreboard players operation #heal tmp = #bolWas tmp
execute if score #clB tmp matches ..99 run scoreboard players operation #heal tmp *= #clHeal tmp
execute if score #clB tmp matches 100.. run scoreboard players operation #heal tmp *= #clHeal2 tmp
scoreboard players operation #heal tmp /= #100 tmp
execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1
scoreboard players set #clHealOk tmp 1
function rlk:player/heal
scoreboard players set #clHealOk tmp 0
particle minecraft:heart ~ ~1.6 ~ 0.2 0.1 0.2 0 1
