# 인벤토리 상세에서 좌클릭 (@s = 플레이어, at @s). 요소 종류: 2 보유 아이템, 7 판매, 8 돌아가기
execute if score @s pkHK matches 2 run return run function rlk:invd/pick
execute if score @s pkHK matches 7 run return run function rlk:invd/sell
execute if score @s pkHK matches 8 run return run function rlk:lvup/exit
