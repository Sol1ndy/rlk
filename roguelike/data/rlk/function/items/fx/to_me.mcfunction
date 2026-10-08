# @s = 맞을 몹. 지금 위치(소환물)에서 이 몹까지 공격 연출 (범위 공격을 대상마다 한 줄기씩)
tag @s add rlk_abt
execute facing entity @s eyes run function rlk:items/fx/shot
tag @s remove rlk_abt
