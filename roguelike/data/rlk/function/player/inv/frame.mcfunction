# 첫 줄: inventory.0 = 캐릭터 정보(머리), 1 = 고유 특성(종이, 추가 설명 포함), 2 = 인벤토리 상세 버튼,
# 3~6 = 각인(같은 개수끼리 묶어 많은 순), 7 = 나머지 각인/각인 요약, 8 = 스탯 정보. 다른 것이 들어 있으면 비운다
execute if items entity @s inventory.0 * unless items entity @s inventory.0 *[minecraft:custom_data~{rlk_char:1b}] run item replace entity @s inventory.0 with air
execute if items entity @s inventory.1 * unless items entity @s inventory.1 *[minecraft:custom_data~{rlk_pas:1b}] run item replace entity @s inventory.1 with air
execute if items entity @s inventory.2 * unless items entity @s inventory.2 *[minecraft:custom_data~{rlk_invd:1b}] run item replace entity @s inventory.2 with air
execute if items entity @s inventory.3 * unless items entity @s inventory.3 *[minecraft:custom_data~{rlk_engi:1b}] run item replace entity @s inventory.3 with air
execute if items entity @s inventory.4 * unless items entity @s inventory.4 *[minecraft:custom_data~{rlk_engi:1b}] run item replace entity @s inventory.4 with air
execute if items entity @s inventory.5 * unless items entity @s inventory.5 *[minecraft:custom_data~{rlk_engi:1b}] run item replace entity @s inventory.5 with air
execute if items entity @s inventory.6 * unless items entity @s inventory.6 *[minecraft:custom_data~{rlk_engi:1b}] run item replace entity @s inventory.6 with air
execute if items entity @s inventory.7 * unless items entity @s inventory.7 *[minecraft:custom_data~{rlk_eng:1b}] run item replace entity @s inventory.7 with air
