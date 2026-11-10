# @s = 플레이어, at 몸 eyes. 닷지가 아닌 무적(dashInvT: 원소폭발 시전 · 로노바 부활 · 추락 뒤)이 막음: 피해 없음, 보상 없음
scoreboard players set #dodged tmp 1
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
particle minecraft:crit ~ ~-0.6 ~ 0.3 0.5 0.3 0.1 2
