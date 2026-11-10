# @s = body: may the balance groggy start now?
execute unless score #ph hr matches 1 unless score #ph hr matches 7 run return fail
execute if score #rp hr matches 1.. run return fail
execute if score #sqn hr matches 1.. run return fail
execute if score #rvw hr matches 1.. run return fail
execute if score #inv hr matches 1.. run return fail
execute if score #fl hr matches 1.. run return fail
execute if entity @s[tag=rlk_hr_ghost] run return fail
execute if entity @s[tag=rlk_mb_inv] run return fail
execute if score #pat hr matches 0 run return 1
execute if score #pat hr matches 1 run return 1
execute if score #pat hr matches 2 run return 1
execute if score #pat hr matches 3 run return 1
execute if score #pat hr matches 4 run return 1
execute if score #pat hr matches 6 run return 1
execute if score #pat hr matches 7 run return 1
execute if score #pat hr matches 11 run return 1
execute if score #pat hr matches 12 run return 1
execute if score #pat hr matches 13 run return 1
return fail
