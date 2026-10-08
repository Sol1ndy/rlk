# 예약된 화살 (@s = 플레이어, at 몸): 두 발짜리 타의 두 번째(bowQ) / 연격의 추가 화살(bowF)
execute if score @s bowQ matches 1.. run scoreboard players remove @s bowQ 1
execute if score @s bowQ matches 0 run function rlk:char/bow/queue_fire
execute if score @s bowF matches 1.. run scoreboard players remove @s bowF 1
execute if score @s bowF matches 0 run function rlk:char/bow/flurry_fire
