# 배치 하나를 무작위로 골라 rlk:room cur 에 복사
execute store result storage rlk:room a.i int 1 run random value 0..7
function rlk:room/pick/copy_boss with storage rlk:room a
