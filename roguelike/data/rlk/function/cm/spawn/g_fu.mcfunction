# 둥실 버섯 무리 5~7 (실행 위치 = 무리장, 실행 방향 = 앞). 방 배치는 #c3Size, 시험(cm/test)은 무작위. 서로 1칸 남짓 붙어서 나옴
execute unless score #c3SizeSet tmp matches 1 store result score #c3Size tmp run random value 5..7
scoreboard players add #c2PackC tmp 1
scoreboard players set #c3InPack tmp 1
scoreboard players set #c3PackLd tmp 0
scoreboard players set #c3Slot tmp 0
function rlk:cm/spawn/fu
scoreboard players set #c2ok tmp 0
execute positioned ^1.1 ^ ^0.4 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.1 ^ ^0.4 run function rlk:cm/spawn/fu
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
scoreboard players set #c2ok tmp 0
execute positioned ^-1.1 ^ ^0.4 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-1.1 ^ ^0.4 run function rlk:cm/spawn/fu
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
scoreboard players set #c2ok tmp 0
execute positioned ^0.6 ^ ^-1.0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0.6 ^ ^-1.0 run function rlk:cm/spawn/fu
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
scoreboard players set #c2ok tmp 0
execute positioned ^-0.6 ^ ^-1.0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-0.6 ^ ^-1.0 run function rlk:cm/spawn/fu
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
execute if score #c3Size tmp matches 6.. run scoreboard players set #c2ok tmp 0
execute if score #c3Size tmp matches 6.. positioned ^0 ^ ^1.2 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c3Size tmp matches 6.. if score #c2ok tmp matches 1 positioned ^0 ^ ^1.2 run function rlk:cm/spawn/fu
execute if score #c3Size tmp matches 6.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
execute if score #c3Size tmp matches 7.. run scoreboard players set #c2ok tmp 0
execute if score #c3Size tmp matches 7.. positioned ^1.3 ^ ^-0.5 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c3Size tmp matches 7.. if score #c2ok tmp matches 1 positioned ^1.3 ^ ^-0.5 run function rlk:cm/spawn/fu
execute if score #c3Size tmp matches 7.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/fu
scoreboard players set #c3InPack tmp 0
