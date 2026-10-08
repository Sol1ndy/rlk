# 기본공격 콤보 1타→2타 (@s = 플레이어, at @s). 콤보 딜레이는 load 의 #comboD12/#comboD21 (공격속도 100% 기준 틱×100)
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
# 스커크: 5타 콤보
execute if score #charN tmp matches 3 run return run function rlk:char/skirk/combo
execute if score #charN tmp matches 4..6 run return run function rlk:char/melee/combo
execute if score #charN tmp matches 8 run return run function rlk:char/melee/combo
scoreboard players operation #step tmp = @s comboStep
execute if score #step tmp matches 0 run function rlk:combat/swing1
execute if score #step tmp matches 1 run function rlk:combat/swing2
execute if score #step tmp matches 0 run function rlk:combat/combo_after1
execute if score #step tmp matches 1 run function rlk:combat/combo_after2
