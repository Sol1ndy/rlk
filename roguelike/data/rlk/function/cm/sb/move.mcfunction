# 땅속에서 자리 옮김(실행 위치 = 확인한 발 자리). 이번 틱의 cm/tick 은 옛 자리에서 돌므로, 리그 부품은 이번 틱 모습 처리
# (sb/rig/tick, 옛 자리에서 부품을 찾은 뒤)가 rlk_c3moved 를 보고 새 자리로 옮김 → 멀리 솟아도 리그를 잃지 않음
tp @s ~ ~ ~
tag @s add rlk_c3moved
scoreboard players set #c3ok tmp 1
