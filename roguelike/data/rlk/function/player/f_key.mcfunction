# @s = 플레이어 (player/hotbar/tick 에서: F 로 무기·스킬·폭발 아이템이 왼손에 넘어옴, 웅크리지 않음). 아이템 회수는 부른 쪽이 한다
execute if score @s vMap matches 1 run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
execute at @e[tag=rlk_body,limit=1] run function rlk:player/dash
