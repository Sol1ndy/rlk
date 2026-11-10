# @s = body: may the balance groggy start now?
execute unless score #azPh mb matches 1..3 run return fail
execute if score #azTr mb matches 1.. run return fail
execute if score #azBur mb matches 1.. run return fail
execute if score #mbFloorHit mb matches 1 run return fail
execute if score #mbCine mb matches 1 run return fail
execute if entity @s[tag=rlk_mb_inv] run return fail
execute if score #azPat mb matches 0..10 run return 1
execute if score #azPat mb matches 27..28 run return 1
execute if score #azPat mb matches 41..46 run return 1
return fail
