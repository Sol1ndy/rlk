# @s = 플레이어. F5 의 우클릭 누름(rcU 1): 지도 화면이면 view/map_tick 에 맡기고, 죽어 있으면 버리고, 아니면 combat/rc_hold
# (처음 틱과 4틱마다 combat/rclick_do). 처리한 뒤 rcU 0
execute if score @s vMap matches 1 run return 0
execute unless score @s dead matches 1 run function rlk:combat/rc_hold
scoreboard players set @s rcU 0
