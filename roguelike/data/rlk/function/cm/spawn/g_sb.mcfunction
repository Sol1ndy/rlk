# 모래 전갈 새끼 6~8 (실행 위치 · 방향): 땅속에서 시작, 무리가 같은 타이머(#c3SbT)로 함께 솟음
execute unless score #c3SizeSet tmp matches 1 store result score #c3Size tmp run random value 6..8
scoreboard players add #c2PackC tmp 1
scoreboard players set #c3InPack tmp 1
scoreboard players set #c3PackLd tmp 0
scoreboard players set #c3Slot tmp 0
execute store result score #c3SbT tmp run random value 20..40
function rlk:cm/spawn/sb
scoreboard players set #c2ok tmp 0
execute positioned ^1.0 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.0 ^ ^0 run function rlk:cm/spawn/sb
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
scoreboard players set #c2ok tmp 0
execute positioned ^-1.0 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^-1.0 ^ ^0 run function rlk:cm/spawn/sb
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
scoreboard players set #c2ok tmp 0
execute positioned ^0 ^ ^1.0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0 ^ ^1.0 run function rlk:cm/spawn/sb
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
scoreboard players set #c2ok tmp 0
execute positioned ^0 ^ ^-1.0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0 ^ ^-1.0 run function rlk:cm/spawn/sb
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
scoreboard players set #c2ok tmp 0
execute positioned ^0.8 ^ ^0.8 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^0.8 ^ ^0.8 run function rlk:cm/spawn/sb
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
execute if score #c3Size tmp matches 7.. run scoreboard players set #c2ok tmp 0
execute if score #c3Size tmp matches 7.. positioned ^-0.8 ^ ^-0.8 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c3Size tmp matches 7.. if score #c2ok tmp matches 1 positioned ^-0.8 ^ ^-0.8 run function rlk:cm/spawn/sb
execute if score #c3Size tmp matches 7.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
execute if score #c3Size tmp matches 8.. run scoreboard players set #c2ok tmp 0
execute if score #c3Size tmp matches 8.. positioned ^0.8 ^ ^-0.8 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c3Size tmp matches 8.. if score #c2ok tmp matches 1 positioned ^0.8 ^ ^-0.8 run function rlk:cm/spawn/sb
execute if score #c3Size tmp matches 8.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/sb
scoreboard players set #c3InPack tmp 0
