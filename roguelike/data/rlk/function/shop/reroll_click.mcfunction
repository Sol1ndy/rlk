# @s = 리롤 인터랙션, at @s. 가까운 플레이어가 리롤 시도
execute at @s as @a[tag=player,limit=1] run function rlk:shop/try_reroll
data remove entity @s attack
