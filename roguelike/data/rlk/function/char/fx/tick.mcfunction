# 진행 중인 모션의 다음 조각 (@s = 플레이어, at 몸)
function rlk:char/fx/run
scoreboard players add @s fxT 1
execute if score @s fxT matches 3.. run scoreboard players set @s fxT 0
