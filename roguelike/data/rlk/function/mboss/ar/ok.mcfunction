# GENERATED dispatcher: rlk:mboss/ar/<aid>/ok of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/ok
execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/ok
execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/ok
execute if score #mbAr mb matches 3 run return run function rlk:mboss/ar/tk_lift/ok
execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/ok
return fail
