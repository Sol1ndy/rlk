# GENERATED dispatcher: rlk:mboss/ar/<aid>/clampw_step of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/clampw_step
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/clampw_step
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/clampw_step
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/clampw_step
