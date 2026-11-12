# 기본공격 아이템(캐릭터의 무기) 복구. 좌클릭 = 기본공격, 우클릭 = 닷지
clear @s *[minecraft:custom_data~{rlk_ui:{role:"attack"}}]
function rlk:char/weapon_item with storage rlk:chars cur.weapon
