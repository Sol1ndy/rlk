# @s = 까마귀 깃이 꽂힌 자리, at @s. 1.5초 뒤 반경 3.5칸에 공격력의 60퍼센트 번개 원소 피해 + 공격력 증가
scoreboard players remove @s life 1
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:0.8f} ~ ~0.3 ~ 0.3 0.2 0.3 0 2
execute if score @s life matches 1.. run return 0
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:1.5f} ~ ~2.2 ~ 0.08 1.6 0.08 0 30
particle minecraft:electric_spark ~ ~0.8 ~ 1.2 0.5 1.2 0.4 30
execute unless score #k134 snd matches 1 run function rlk:snd/f142
scoreboard players operation #tenguT itv = #tenguDur tmp
function rlk:items/proc/tengu_boom
kill @s
