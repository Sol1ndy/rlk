# 졸개 무리 4~6 (실행 위치 = 무리장, 실행 방향 = 앞). 방 배치는 #c2Size, 시험(cm/test)은 무작위
execute unless score #c2SizeSet tmp matches 1 store result score #c2Size tmp run random value 4..6
scoreboard players add #c2PackC tmp 1
scoreboard players set #c2InPack tmp 1
scoreboard players set #c2PackLd tmp 0
function rlk:cm/spawn/ns
scoreboard players set #c2ok tmp 0
execute positioned ^1.5 ^ ^0.5 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.5 ^ ^0.5 run function rlk:cm/spawn/ns
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/ns
scoreboard players set #c2ok tmp 0
execute positioned ^-1.5 ^ ^0.5 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-1.5 ^ ^0.5 run function rlk:cm/spawn/ns
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/ns
scoreboard players set #c2ok tmp 0
execute positioned ^0.8 ^ ^-1.3 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0.8 ^ ^-1.3 run function rlk:cm/spawn/ns
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/ns
execute if score #c2Size tmp matches 5.. run scoreboard players set #c2ok tmp 0
execute if score #c2Size tmp matches 5.. positioned ^-0.8 ^ ^-1.3 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2Size tmp matches 5.. if score #c2ok tmp matches 1 positioned ^-0.8 ^ ^-1.3 run function rlk:cm/spawn/ns
execute if score #c2Size tmp matches 5.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/ns
execute if score #c2Size tmp matches 6.. run scoreboard players set #c2ok tmp 0
execute if score #c2Size tmp matches 6.. positioned ^0 ^ ^1.6 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2Size tmp matches 6.. if score #c2ok tmp matches 1 positioned ^0 ^ ^1.6 run function rlk:cm/spawn/ns
execute if score #c2Size tmp matches 6.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/ns
scoreboard players set #c2InPack tmp 0
