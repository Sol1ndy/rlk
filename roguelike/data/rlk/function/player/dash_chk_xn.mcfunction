# 위치 = 옮겨 갈 자리(몸의 발밑 가운데). x축 -쪽 면이 블록에 닿으면 #dblk tmp = 1 (면은 몸보다 0.0001 바깥, 옆 폭은 0.0001 안쪽)
execute unless block ~-0.3001 ~0.2 ~-0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~0.2 ~0 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~0.2 ~0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.0 ~-0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.0 ~0 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.0 ~0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.75 ~-0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.75 ~0 #rlk:dash_pass run scoreboard players set #dblk tmp 1
execute unless block ~-0.3001 ~1.75 ~0.2999 #rlk:dash_pass run scoreboard players set #dblk tmp 1
