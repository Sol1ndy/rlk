# GENERATED dispatcher: rlk:mboss/ar/<aid>/full_rim of the fight arena (#mbAr mb = arena n; unset or 0 = the plaza).
$execute unless score #mbAr mb matches 1.. run return run function rlk:mboss/ar/plaza/full_rim {kp:$(kp)}
$execute if score #mbAr mb matches 1 run return run function rlk:mboss/ar/az_cavern/full_rim {kp:$(kp)}
$execute if score #mbAr mb matches 2 run return run function rlk:mboss/ar/ap_oasis/full_rim {kp:$(kp)}
$execute if score #mbAr mb matches 9 run return run function rlk:mboss/ar/cp_test/full_rim {kp:$(kp)}
