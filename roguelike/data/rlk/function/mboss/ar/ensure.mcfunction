# GENERATED dispatcher: rlk:mboss/ar/<aid>/ensure of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/ensure
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/ensure
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/ensure
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/ensure
return fail
