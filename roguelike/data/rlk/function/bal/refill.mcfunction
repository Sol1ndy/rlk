# API for the boss modules: @s = boss whose own mechanic groggy (a break, a stun, a down) starts — the balance gauge
# is full again and a pending balance groggy is dropped, so the two never chain. Nothing while a balance groggy runs.
execute unless score @s balMax matches 1.. run return 0
execute if score @s grgT matches 1.. run return 0
tag @s remove rlk_bal_pend
scoreboard players operation @s bal = @s balMax
scoreboard players set @s balT 0
scoreboard players set @s balF 0
function rlk:bal/ui/draw
