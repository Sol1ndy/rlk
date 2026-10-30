# GENERATED dispatcher: rlk:mboss/ar/<aid>/box_absorb of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/box_absorb
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/box_absorb
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/box_absorb
execute if score #mbAr mb matches 3 run return run function rlk:mboss/ar/tk_lift/box_absorb
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/box_absorb
