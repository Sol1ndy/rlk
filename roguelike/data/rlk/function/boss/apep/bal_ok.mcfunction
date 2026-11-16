# @s = body: may the balance groggy start now?
execute unless score #apPh mb matches 1 unless score #apPh mb matches 3 run return fail
execute if score #apTr mb matches 1.. run return fail
execute if score #mbFloorHit mb matches 1 run return fail
execute if score #mbCine mb matches 1 run return fail
execute if entity @s[tag=rlk_mb_inv] run return fail
execute if score #apPid mb matches 0..7 run return 1
execute if score #apPid mb matches 10 run return 1
execute if score #apPid mb matches 31 run return 1
execute if score #apPid mb matches 33..36 run return 1
return fail
