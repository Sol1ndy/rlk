# 유금화광이 붙은 적이 죽음 (@s = 죽는 몹, at @s): 12칸 안의 가장 가까운 다른 적이 남은 시간을 이어받는다
execute store result score #ynow tmp run time query gametime
execute unless score @s aurEnd > #ynow tmp run return 0
tag @s add rlk_dying
scoreboard players operation @e[tag=rlk_mob,tag=!rlk_dying,distance=..12,sort=nearest,limit=1] aurEnd > @s aurEnd
tag @s remove rlk_dying
