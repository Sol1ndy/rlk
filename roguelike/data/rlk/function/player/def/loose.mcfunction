# @s = 플레이어, at 몸 eyes. 넓은 닷지(일반 몹의 공격을 닷지를 누른 지 #dgPW ~ #dgLW 틱 사이에): 피해 없음, 보상 없음
scoreboard players set #dodged tmp 1
execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
particle minecraft:crit ~ ~-0.6 ~ 0.3 0.5 0.3 0.1 2
