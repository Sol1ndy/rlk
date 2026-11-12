# Test 38: her balance = 1 pip (the next perfect parry / burst hit breaks her).
execute if score #mbSt mb matches 0 run function rlk:boss/scarlet/core/intro/done
execute if score @s grgT matches 1.. run return 0
tag @s remove rlk_bal_pend
scoreboard players set @s bal 1
scoreboard players operation @s balT = #rd3 bal
function rlk:bal/ui/draw
