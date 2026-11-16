# 몹이 설 수 있는 자리인가(실행 위치 = 발): 발 · 머리 칸이 비고 발밑이 막혀 있음. 2챕터 집 · 가게 안(가문비나무 판자 바닥)은 안 됨
execute unless block ~ ~ ~ #rlk:dash_pass run return 0
execute unless block ~ ~1 ~ #rlk:dash_pass run return 0
execute if block ~ ~-1 ~ #rlk:dash_pass run return 0
execute if score #th room matches 4 if block ~ ~-1 ~ minecraft:spruce_planks run return 0
return 1
