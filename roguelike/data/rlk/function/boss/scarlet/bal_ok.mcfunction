# @s = body: may the balance groggy start now? (hr_design §1.3; a refused break stays pending: lane B starts it at
# the first allowed tick.)
execute unless score #ph hr matches 1 unless score #ph hr matches 7 run return fail
execute if score #rp hr matches 1.. run return fail
execute if score #sqn hr matches 1.. run return fail
execute if score #rvw hr matches 1.. run return fail
execute if score #inv hr matches 1.. run return fail
execute if score #fl hr matches 1.. run return fail
execute if entity @s[tag=rlk_hr_ghost] run return fail
execute if entity @s[tag=rlk_mb_inv] run return fail
execute if score #pat hr matches 4 if score #pt hr matches 2..20 run return fail
execute if score #pat hr matches 7 if score #pt hr matches 2..22 run return fail
execute if score #pat hr matches 17 if score #pt hr matches 2..46 run return fail
execute if score #pat hr matches 18 if score #pt hr matches 16.. run return fail
execute if score #pat hr matches 13 if score #pt hr matches 24..26 run return fail
execute if score #pat hr matches 6 if score #pt hr matches 26..28 run return fail
execute if score #pat hr matches 15 if score #pt hr matches 20..22 run return fail
execute if score #pat hr matches 14 if score #pt hr matches 20..22 run return fail
execute if score #pat hr matches 12 if score #pt hr matches 24..46 run return fail
execute if score #pat hr matches 16 if score #pt hr matches 14..16 run return fail
execute if score #pat hr matches 5 if score #pt hr matches 0..4 run return fail
execute if score #pat hr matches 16 if score #mx_pre hr matches 1.. run return fail
return 1
