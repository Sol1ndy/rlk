# 불꽃놀이: 타마다 다른 자세 (@s = 플레이어, at 몸, #step = 0~4)
#   화살이 나가는 자리 #bOff(0 가운데 / 1 오른쪽 / 2 왼쪽 / 3 위) · 두 발짜리 타의 두 번째 화살 #bOff2 · 마지막 타 #bFin
scoreboard players operation #fxId tmp = #step tmp
execute if score #fxId tmp matches 5.. run scoreboard players set #fxId tmp 4
scoreboard players add #fxId tmp 60
execute if score @s yoiSk matches 1.. run scoreboard players add #fxId tmp 10
function rlk:char/fx/play
execute if score #step tmp matches 0 run scoreboard players set #bOff tmp 1
execute if score #step tmp matches 0 run scoreboard players set #bOff2 tmp 2
execute if score #step tmp matches 2 run scoreboard players set #bOff tmp 3
execute if score #step tmp matches 3 run scoreboard players set #bOff tmp 2
execute if score #step tmp matches 3 run scoreboard players set #bOff2 tmp 1
execute if score #step tmp matches 4.. run scoreboard players set #bFin tmp 1
