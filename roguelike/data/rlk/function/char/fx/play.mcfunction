execute if score #charN tmp matches 3 run return 0
execute if score #charN tmp matches 5 run return 0
# 모션 시작 (@s = 플레이어, at 몸, 입력: #fxId tmp). 첫 조각은 바로, 나머지는 다음 틱부터 char/fx/tick 이 그린다
scoreboard players operation @s fxId = #fxId tmp
scoreboard players set @s fxT 0
function rlk:char/fx/run
scoreboard players set @s fxT 1
