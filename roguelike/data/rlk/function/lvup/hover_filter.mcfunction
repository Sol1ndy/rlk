# 요소 종류: 1 선택지, 2 인벤 아이템, 3 리롤, 4 넘기기, 5 확인, 6 취소, 9 현재 캐릭터(설명만)
# 인벤토리 상세(모드 4)의 요소: 2 인벤 아이템, 7 판매, 8 돌아가기 (그 화면에는 이 셋만 있어 따로 거르지 않음)
# 모드: 1 고르는 중(선택지·인벤·리롤·넘기기), 2 확인 창(확인·취소만), 3 바꿀 아이템 고르기(인벤·취소만)
execute if score @s pkMode matches 2 unless score #pkK tmp matches 5..6 run scoreboard players set #pkK tmp 0
# 모드 5 = 교체 확인 창(확인·취소만)
execute if score @s pkMode matches 5 unless score #pkK tmp matches 5..6 run scoreboard players set #pkK tmp 0
execute if score @s pkMode matches 3 unless score #pkK tmp matches 2 unless score #pkK tmp matches 6 run scoreboard players set #pkK tmp 0
execute if score #pkK tmp matches 0 run scoreboard players set #pkI tmp 0
