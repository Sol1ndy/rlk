# 남은 후보 중 하나를 뽑아 선택 오브젝트로 (위치 = 현재 실행 위치)
execute store result score #n tmp run data get storage rlk:room pool
execute store result score #r tmp run random value 0..999
scoreboard players operation #r tmp %= #n tmp
execute store result storage rlk:room a.i int 1 run scoreboard players get #r tmp
function rlk:room/choice2 with storage rlk:room a
