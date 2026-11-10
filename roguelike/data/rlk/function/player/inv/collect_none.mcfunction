# (player/inv/sync 의 빠른 길) collect_loop 를 건너뛸 때 그것이 남기던 점수를 그대로: 모든 실물이 order 에 있으면 마지막으로 센 id 의
# 개수(#c1 · #c2, order_count2)와 남은 수(#left, collect_check)는 0. #c2 는 load 의 상수 #c2 tmp(= 2, char/nefer/cat_tick 이 읽음)와
# 이름이 같아 예전부터 인벤 정리 때마다 덮였다 — 동작을 바꾸지 않으려고 여기서도 같게 둔다
scoreboard players set #c1 tmp 0
scoreboard players set #c2 tmp 0
scoreboard players set #left tmp 0
