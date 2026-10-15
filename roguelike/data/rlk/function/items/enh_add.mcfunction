# macro: id → 그 아이템의 강화 단계 +1 (최대 3). rlk:pinv enh.<id> 와 점수 <id> enhL (효과 배율 계산용)
scoreboard players set #enh tmp 0
$execute if data storage rlk:pinv enh.$(id) store result score #enh tmp run data get storage rlk:pinv enh.$(id)
scoreboard players add #enh tmp 1
execute if score #enh tmp matches 4.. run scoreboard players set #enh tmp 3
$execute store result storage rlk:pinv enh.$(id) int 1 run scoreboard players get #enh tmp
$scoreboard players operation $(id) enhL = #enh tmp
# 효과 상수 · 설명 숫자 다시 계산
$execute if data storage rlk:tune t.$(id) run function rlk:items/tune/apply {id:"$(id)"}
