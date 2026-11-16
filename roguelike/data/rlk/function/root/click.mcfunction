# 나무뿌리 화면의 좌클릭 (@s = 플레이어). 14 각인 카드 = 기적 받기, 8 돌아가기
execute if score @s pkHK matches 8 run return run function rlk:lvup/exit
execute if score @s pkHK matches 14 run return run function rlk:root/take
