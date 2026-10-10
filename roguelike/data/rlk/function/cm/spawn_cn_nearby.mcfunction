# 같은 높이의 후보 9칸만 확인. 소환 함수 자체가 3x3 평지/머리 공간을 검사한다.
scoreboard players set #cnSpawnOk tmp 0
function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~1 ~ ~0 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~-1 ~ ~0 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~0 ~ ~1 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~0 ~ ~-1 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~1 ~ ~1 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~-1 ~ ~1 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~1 ~ ~-1 run function rlk:cm/spawn/cn
execute if score #cnSpawnOk tmp matches 0 positioned ~-1 ~ ~-1 run function rlk:cm/spawn/cn
