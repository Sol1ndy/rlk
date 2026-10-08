# 각인 아이템의 총 개수가 달라짐(버림·집음 등) → 다시 만들고 기준 개수를 새로 적는다
function rlk:engravings/info_build
execute store result score @s engItems run clear @s *[minecraft:custom_data~{rlk_engi:1b}] 0
