# @s = 몹. 0 피해를 아바타가 준 것으로 처리 → 몹이 아바타를 공격 대상으로 삼는다
tag @s remove rlk_agq
damage @s 0 minecraft:generic by @e[tag=rlk_av,limit=1]
