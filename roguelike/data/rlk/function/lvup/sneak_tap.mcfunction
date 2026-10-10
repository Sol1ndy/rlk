# (@s = 플레이어) 고를 것이 있거나 선택 공간 안이면 토글. 아니면 아무 일 없음(웅크림은 다른 데 안 씀)
execute unless score @s pkMode matches 1.. unless score @s pkPending matches 1.. run return 0
execute at @s run function rlk:lvup/toggle
scoreboard players set @s uiCd 10
