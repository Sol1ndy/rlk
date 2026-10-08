# @s = 플레이어. 금단의 도서 보유 시에만 페이지 획득
execute if score @s it_forbidden_book matches 1.. run scoreboard players add @s forbPages 1
