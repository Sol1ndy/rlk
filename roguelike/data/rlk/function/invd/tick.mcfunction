# 인벤토리 상세 버튼 (@s = 플레이어, 매 틱. 개발자 모드에서는 호출되지 않음)
# 버튼은 인벤토리 첫 줄 2번 칸(inventory.2)에 고정. 제자리에 없으면 = 눌러서 커서로 집었거나 다른 칸으로 옮긴 것
execute unless items entity @s inventory.2 minecraft:chest[minecraft:custom_data~{rlk_invd:1b}] run function rlk:invd/missing
execute if score @s pkMode matches 4 if score @s pkConf matches 1 unless score @s pkHK matches 7 run function rlk:invd/sell_unask
