# 배치 하나를 무작위로 골라 rlk:room cur 에 복사
execute store result storage rlk:room a.i int 1 run random value 0..11
function rlk:room/pick/copy_first with storage rlk:room a
