# 콤보 진행 (@s = 플레이어, at 몸). 타 수 = #naSteps(캐릭터의 na_coef 가 정함). 타마다 고유 모션(char/fx), 마지막 타 뒤에는 긴 간격(#comboD21)
scoreboard players operation #step tmp = @s comboStep
# 모션: 클로린드 30 + 타 번호 / 아를레키노 40 + 타 번호(붉은 가면 중에는 50 +)
scoreboard players operation #fxId tmp = #step tmp
execute if score #charN tmp matches 4 run scoreboard players add #fxId tmp 30
execute if score #charN tmp matches 5 run scoreboard players add #fxId tmp 40
execute if score #charN tmp matches 6 run scoreboard players add #fxId tmp 80
execute if score #charN tmp matches 8 run scoreboard players add #fxId tmp 100
execute if score #charN tmp matches 6 if score @s nvP matches 1.. run scoreboard players add #fxId tmp 10
execute if score #charN tmp matches 5 if score @s arM matches 1 run scoreboard players add #fxId tmp 10
function rlk:char/fx/play
scoreboard players operation #last tmp = #naSteps tmp
scoreboard players remove #last tmp 1
execute if score #step tmp < #last tmp run function rlk:combat/combo_after1
execute if score #step tmp < #last tmp run scoreboard players operation @s comboStep = #step tmp
execute if score #step tmp < #last tmp run scoreboard players add @s comboStep 1
execute if score #step tmp >= #last tmp run function rlk:combat/combo_after2
