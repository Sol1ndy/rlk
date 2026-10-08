# @s = 닫힌 문(검은 콘크리트). 전투가 시작된 구역 쪽 면에 봉인 무늬
execute if score @s da = #combat room run function rlk:room/seal_a with entity @s data
execute if score @s db = #combat room run function rlk:room/seal_b with entity @s data
