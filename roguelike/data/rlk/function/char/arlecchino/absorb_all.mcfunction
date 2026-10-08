# 모든 적의 핏값을 회수 (@s = 플레이어)
execute store result score #ynow tmp run time query gametime
execute as @e[tag=rlk_mob] if score @s arDir > #ynow tmp run function rlk:char/arlecchino/dir_take
