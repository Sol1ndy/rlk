# 판정 끝(player/def/judge): 한 번 쓰는 피해 문맥을 지우고 공격자 표시를 뗀다(맞음 · 피함 모두)
scoreboard players set #hcK tmp 0
scoreboard players set #hcC tmp 0
scoreboard players set #hcNP tmp 0
scoreboard players set #hcND tmp 0
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
