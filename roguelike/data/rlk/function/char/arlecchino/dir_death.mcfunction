# 핏값이 붙은 적이 죽음 (@s = 죽는 몹): 자동 회수
execute store result score #ynow tmp run time query gametime
execute if score @s arDir > #ynow tmp run function rlk:char/arlecchino/dir_take
