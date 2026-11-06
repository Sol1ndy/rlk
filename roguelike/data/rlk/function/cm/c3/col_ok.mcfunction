# 한 칸 기둥이 지나갈 수 있는가 (실행 위치 = 발 높이의 그 칸): 몸 · 머리 칸이 비고(벽 · 문 · 철창 · 물 아님) 발밑 1~2칸 안에 바닥. 한 칸 오르막도 됨
execute if block ~ ~0.4 ~ #rlk:dash_pass if block ~ ~1.4 ~ #rlk:dash_pass unless block ~ ~-0.6 ~ #rlk:cm_pass run return 1
execute if block ~ ~0.4 ~ #rlk:dash_pass if block ~ ~1.4 ~ #rlk:dash_pass unless block ~ ~-1.6 ~ #rlk:cm_pass run return 1
execute unless block ~ ~0.4 ~ #rlk:cm_pass if block ~ ~1.4 ~ #rlk:dash_pass if block ~ ~2.4 ~ #rlk:dash_pass run return 1
return 0
