# 밤 순찰 중 적중: 원소 입자 1개 (@s = 플레이어, at 몸). #clPcGap 틱마다, 스킬 한 번에 #clPcMax 개까지
execute if score @s clPcCd matches 1.. run return 0
execute if score @s clPcN >= #clPcMax tmp run return 0
scoreboard players operation @s clPcCd = #clPcGap tmp
scoreboard players add @s clPcN 1
function rlk:char/particles {n:1,el:3}
