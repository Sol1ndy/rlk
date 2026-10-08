# 콤보 진행 (@s = 플레이어, at 몸): 타마다 고유 모션(char/fx), 5타 뒤에는 긴 간격(#comboD21)
scoreboard players operation #step tmp = @s comboStep
# 모션: 10 + 타 번호(일곱빛 섬광 중에는 20 +)
scoreboard players operation #fxId tmp = #step tmp
execute if score #fxId tmp matches 5.. run scoreboard players set #fxId tmp 4
scoreboard players add #fxId tmp 10
execute if score @s skM matches 1.. run scoreboard players add #fxId tmp 10
function rlk:char/fx/play
execute if score #step tmp matches ..3 run function rlk:combat/combo_after1
execute if score #step tmp matches ..3 run scoreboard players operation @s comboStep = #step tmp
execute if score #step tmp matches ..3 run scoreboard players add @s comboStep 1
execute if score #step tmp matches 4.. run function rlk:combat/combo_after2
