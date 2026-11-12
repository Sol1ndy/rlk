# 몸(실행 위치)에서 고리 자리 쪽 0.9 · 1.8칸이 몸 높이로 비었는가(벽 · 문 너머로는 안 솟음)
execute unless block ^ ^0.5 ^0.9 #rlk:dash_pass run return 0
execute unless block ^ ^1.2 ^0.9 #rlk:dash_pass run return 0
execute unless block ^ ^0.5 ^1.8 #rlk:dash_pass run return 0
execute unless block ^ ^1.2 ^1.8 #rlk:dash_pass run return 0
return 1
