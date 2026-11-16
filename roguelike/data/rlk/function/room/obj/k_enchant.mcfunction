# 인챈트 구역 오브젝트 (위치 = 실행 위치). 강화 횟수 2~4번(oarg, 쓸 때마다 줄어든다)
scoreboard players set #oact tmp 5
execute store result score #oarg tmp run random value 2..4
execute store result storage rlk:room a.n int 1 run scoreboard players get #oarg tmp
function rlk:room/obj/k_enchant2 with storage rlk:room a
