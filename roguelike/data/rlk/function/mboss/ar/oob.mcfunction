# GENERATED dispatcher: rlk:mboss/ar/<aid>/oob of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/oob
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/oob
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/oob
execute if score #mbAr mb matches 3 run return run function rlk:mboss/ar/tk_lift/oob
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/oob
