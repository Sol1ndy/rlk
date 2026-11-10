# @s = 플레이어, at 몸 eyes. 퍼펙트 닷지(닷지를 누른 지 #dgPW 틱 안에 맞을 공격, 모든 적): 피해 없음. 닷지 한 번에 보상 한 번
# (원소 에너지 #dgEn, 붉은 화면 · 잔상 · 소리; player/def/pd_go), 화무십일홍 「검신합일」은 피할 때마다(그 재사용 대기 안에서)
scoreboard players set #dodged tmp 1
scoreboard players set #pdg tmp 1
execute unless score @s dgRw = @s dgAt run function rlk:player/def/pd_go
execute if score @s it_sword_hwamu matches 1.. unless score #hwCtrCd itv matches 1.. run function rlk:items/proc/hw_ctr_q
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
