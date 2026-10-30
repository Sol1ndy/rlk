# 에르미타 단검 용병 3~4 (실행 위치 · 방향). 자리 번호 = 몸 둘레를 도는 순서
execute unless score #c3SizeSet tmp matches 1 store result score #c3Size tmp run random value 3..4
scoreboard players add #c2PackC tmp 1
scoreboard players set #c3InPack tmp 1
scoreboard players set #c3PackLd tmp 0
scoreboard players set #c3Slot tmp 0
function rlk:cm/spawn/em
scoreboard players set #c2ok tmp 0
execute positioned ^1.6 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.6 ^ ^0 run function rlk:cm/spawn/em
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/em
scoreboard players set #c2ok tmp 0
execute positioned ^-1.6 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-1.6 ^ ^0 run function rlk:cm/spawn/em
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/em
execute if score #c3Size tmp matches 4.. run scoreboard players set #c2ok tmp 0
execute if score #c3Size tmp matches 4.. positioned ^0 ^ ^-1.6 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c3Size tmp matches 4.. if score #c2ok tmp matches 1 positioned ^0 ^ ^-1.6 run function rlk:cm/spawn/em
execute if score #c3Size tmp matches 4.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/em
scoreboard players set #c3InPack tmp 0
