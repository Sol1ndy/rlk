# 기본공격 아이템(캐릭터의 무기) 복구. 좌클릭 = 기본공격, 우클릭 = 대쉬(활은 조준 사격)
clear @s *[minecraft:custom_data~{rlk_ui:{role:"attack"}}]
execute unless score #wType tmp matches 2 run function rlk:char/weapon_item with storage rlk:chars cur.weapon
execute if score #wType tmp matches 2 run function rlk:char/weapon_item_bow with storage rlk:chars cur.weapon
