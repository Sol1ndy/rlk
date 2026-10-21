# GENERATED dispatcher: rlk:mboss/ar/<aid>/sweep of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/sweep
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/sweep
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/sweep
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/sweep
