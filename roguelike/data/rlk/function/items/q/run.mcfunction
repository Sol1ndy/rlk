# @s = 예약 표식, at @s (iqK = 종류, iqV = 값)
execute if score @s iqK matches 1 run function rlk:items/proc/skandha_hit
execute if score @s iqK matches 2 run function rlk:items/proc/orb_hit
execute if score @s iqK matches 4 run function rlk:char/yoimiya/aur_boom
execute if score @s iqK matches 5 run function rlk:items/proc/mech_hit
kill @s

