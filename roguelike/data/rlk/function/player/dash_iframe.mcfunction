# 대쉬 무적 (@s = 플레이어): 피해 무시
scoreboard players set #dodged tmp 1
# 화무십일홍: 대쉬로 흘려내면 다음 틱에 반격(검신합일)
execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q
particle minecraft:crit ~ ~1 ~ 0.3 0.5 0.3 0.1 2
