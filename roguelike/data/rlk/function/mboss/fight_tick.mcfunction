# balance gauge (tools/build_balance.py): balT >= 1 while pips are missing, groggy or pending -> fight_bal (one test
# per tick otherwise; a paused fight runs neither, so the gauge clocks stop too)
execute if score @s balT matches 1.. run return run function rlk:mboss/fight_bal
function rlk:mboss/d/tick
execute if score #mbSt mb matches 1 unless score #mbNoLeash mb matches 1 run function rlk:mboss/mv/leash
