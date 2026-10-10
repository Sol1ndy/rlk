# 차지 시작 공통: 경직 면역(rlk_cmch) + 경직 풀기 + 멈춤
tag @s add rlk_cmch
execute if score @s stunT matches 1.. run function rlk:mob/unstun
scoreboard players set #hold tmp 1
