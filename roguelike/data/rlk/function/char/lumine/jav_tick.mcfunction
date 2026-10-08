# @s = 날아가는 투창, at @s (매 틱). 틱당 0.85칸씩 두 번 이동, 앞쪽의 적을 향해 살짝 휨
scoreboard players add @s life 1
execute if score @s life matches 24.. run return run function rlk:char/lumine/jav_break
# 살짝 추적: 4.5칸 앞 지점 반경 4칸 안의 가장 가까운 적 쪽으로 조금 꺾는다
execute positioned ^ ^ ^4.5 if entity @e[tag=rlk_mob,distance=..4] run function rlk:char/lumine/jav_home
scoreboard players set #jend tmp 0
function rlk:char/lumine/jav_step
execute if score #jend tmp matches 0 run function rlk:char/lumine/jav_step
execute if score #jend tmp matches 0 at @s run particle minecraft:snowflake ~ ~ ~ 0.05 0.05 0.05 0.01 2
