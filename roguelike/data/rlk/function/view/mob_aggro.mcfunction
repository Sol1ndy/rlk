# @s = 몹. 0 피해를 아바타가 준 것으로 처리 → 몹이 아바타를 공격 대상으로 삼는다
# 로노바가 쓰러져 있는 동안은 미룸(태그 유지 → 일어난 뒤에)
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
# 커스텀 몹: 미끼를 노리게
execute if entity @s[tag=rlk_cmb] run return run function rlk:cm/aggro_force
tag @s remove rlk_agq
damage @s 0 minecraft:generic by @e[tag=rlk_av,limit=1]
