# GENERATED dispatcher: rlk:mboss/ar/<aid>/tp_in of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/tp_in
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/tp_in
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/tp_in
