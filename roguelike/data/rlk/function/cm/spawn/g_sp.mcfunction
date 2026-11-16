# 창병 대열 3 (실행 위치 = 가운데, 실행 방향 = 앞): 왼쪽 ^1.6 · 가운데 · 오른쪽 ^-1.6
scoreboard players add #c2PackC tmp 1
scoreboard players set #c2InPack tmp 1
scoreboard players set #c2Slot tmp 1
function rlk:cm/spawn/sp
scoreboard players set #c2Slot tmp 0
scoreboard players set #c2ok tmp 0
execute positioned ^1.6 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.6 ^ ^0 run function rlk:cm/spawn/sp
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sp
scoreboard players set #c2Slot tmp 2
scoreboard players set #c2ok tmp 0
execute positioned ^-1.6 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-1.6 ^ ^0 run function rlk:cm/spawn/sp
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sp
scoreboard players set #c2InPack tmp 0
