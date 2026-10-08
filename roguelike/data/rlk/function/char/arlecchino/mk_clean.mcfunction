# 표식 정리 (@s = 플레이어): 핏값이 끝났거나(만료·회수) 몹이 사라진 표식을 지운다
execute store result score #ynow tmp run time query gametime
tag @e[tag=rlk_armk] add rlk_armk_x
execute as @e[tag=rlk_mob,tag=rlk_armd] if score @s arDir > #ynow tmp on passengers run tag @s[tag=rlk_armk] remove rlk_armk_x
kill @e[tag=rlk_armk_x]
execute as @e[tag=rlk_armd] unless score @s arDir > #ynow tmp run tag @s remove rlk_armd
