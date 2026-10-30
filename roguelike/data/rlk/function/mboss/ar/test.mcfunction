# GENERATED dispatcher: rlk:mboss/ar/<aid>/test of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/test
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/test
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/test
execute if score #mbAr mb matches 3 run return run function rlk:mboss/ar/tk_lift/test
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/test
