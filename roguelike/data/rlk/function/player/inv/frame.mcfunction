# 첫 줄: inventory.0 = 캐릭터 정보(머리), inventory.4 = 인벤토리 상세 버튼, inventory.1 = 고유 특성(종이), inventory.2 = 캐릭터 추가 설명(종이), 나머지 inventory.3~6 = 빈칸, inventory.7 = 각인 정보. 뭔가 있을 때만 비움
execute if items entity @s inventory.0 * unless items entity @s inventory.0 *[minecraft:custom_data~{rlk_char:1b}] run item replace entity @s inventory.0 with air
execute if items entity @s inventory.1 * unless items entity @s inventory.1 *[minecraft:custom_data~{rlk_pas:1b}] run item replace entity @s inventory.1 with air
execute if items entity @s inventory.2 * unless items entity @s inventory.2 *[minecraft:custom_data~{rlk_ext:1b}] run item replace entity @s inventory.2 with air
execute if items entity @s inventory.3 * run item replace entity @s inventory.3 with air
execute if items entity @s inventory.4 * unless items entity @s inventory.4 *[minecraft:custom_data~{rlk_invd:1b}] run item replace entity @s inventory.4 with air
execute if items entity @s inventory.5 * run item replace entity @s inventory.5 with air
execute if items entity @s inventory.6 * run item replace entity @s inventory.6 with air
execute if items entity @s inventory.7 * unless items entity @s inventory.7 *[minecraft:custom_data~{rlk_eng:1b}] run item replace entity @s inventory.7 with air
