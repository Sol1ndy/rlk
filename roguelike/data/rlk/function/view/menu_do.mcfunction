# G 메뉴: 지도는 열기/닫기. 다른 화면으로 갈 때 지도 복귀 처리를 먼저 한다.
scoreboard players operation #mn tmp = @s rlkMenu
scoreboard players set @s rlkMenu 0
execute if score #mn tmp matches 1 run return run function rlk:view/map_toggle
execute if score #mn tmp matches 2 if score @s vMap matches 1 run function rlk:view/map_close
execute if score #mn tmp matches 2 at @s run function rlk:lvup/toggle
