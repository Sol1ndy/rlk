# 아이템 영역 뒤쪽(order 길이 초과) 칸 비우기
$execute if items entity @s inventory.$(slnum) * run item replace entity @s inventory.$(slnum) with air
