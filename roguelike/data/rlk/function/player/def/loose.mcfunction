# @s = 플레이어, at 몸 eyes. 넓은 닷지(일반 몹의 공격을 닷지를 누른 지 #dgPW ~ #dgLW 틱 사이에): 피해 없음, 보상 없음(재사용 대기만
# 돌려받는다: player/def/dg_refund, 닷지 한 번에 한 번)
scoreboard players set #dodged tmp 1
execute unless score @s dgAt = #dgRf cb run function rlk:player/def/dg_refund
execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q
particle minecraft:crit ~ ~-0.6 ~ 0.3 0.5 0.3 0.1 2
