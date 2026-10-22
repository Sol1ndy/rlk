# 인챈트 화면의 좌클릭 (@s = 플레이어). 2 보유 아이템 = 강화, 8 돌아가기
execute if score @s pkHK matches 8 run return run function rlk:lvup/exit
execute if score @s pkHK matches 2 run return run function rlk:ench/pick
