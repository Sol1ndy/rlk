# 번개 슬라임 2~3 (실행 위치 · 방향). 방 배치는 #c2Size, 시험은 무작위
execute unless score #c2SizeSet tmp matches 1 store result score #c2Size tmp run random value 2..3
function rlk:cm/spawn/sl
scoreboard players set #c2ok tmp 0
execute positioned ^1.8 ^ ^0 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2ok tmp matches 1 positioned ^1.8 ^ ^0 run function rlk:cm/spawn/sl
execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/sl
execute if score #c2Size tmp matches 3.. run scoreboard players set #c2ok tmp 0
execute if score #c2Size tmp matches 3.. positioned ^-1.8 ^ ^-0.4 if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1
execute if score #c2Size tmp matches 3.. if score #c2ok tmp matches 1 positioned ^-1.8 ^ ^-0.4 run function rlk:cm/spawn/sl
execute if score #c2Size tmp matches 3.. if score #c2ok tmp matches 0 run function rlk:cm/spawn/sl
