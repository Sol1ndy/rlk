# 위치 = 옮겨 갈 자리(몸의 발밑 가운데). z축 +쪽 면이 블록에 닿으면 #dblk tmp = 1 (면은 몸보다 0.0001 바깥, 옆 폭은 0.0001 안쪽)
# 발 높이(+0.0001)에도 면 바깥을 본다: 발이 바닥보다 낮게 서 있을 때(진흙 등 14/16 블록 위, 점프 중 y 소수부 0.8 이상) 옆의 꽉 찬 블록 속으로 발을 넣으면 몸이 그 블록을 뚫고 한 칸 가라앉으므로 막는다(높이가 0.8~1 인 #rlk:low_top 블록은 예전처럼 +0.2 줄이 판단)
execute unless block ~-0.2999 ~0.0001 ~0.3001 #rlk:dash_pass unless block ~-0.2999 ~0.0001 ~0.3001 #rlk:low_top run scoreboard players set #dblk tmp 1
execute unless block ~0 ~0.0001 ~0.3001 #rlk:dash_pass unless block ~0 ~0.0001 ~0.3001 #rlk:low_top run scoreboard players set #dblk tmp 1
execute unless block ~0.2999 ~0.0001 ~0.3001 #rlk:dash_pass unless block ~0.2999 ~0.0001 ~0.3001 #rlk:low_top run scoreboard players set #dblk tmp 1
execute unless block ~-0.2999 ~0.2 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0 ~0.2 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0.2999 ~0.2 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.2999 ~1.0 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0 ~1.0 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0.2999 ~1.0 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.2999 ~1.75 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0 ~1.75 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~0.2999 ~1.75 ~0.3001 #rlk:dash_pass run scoreboard players set #dblk tmp 1
