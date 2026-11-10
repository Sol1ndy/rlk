# @s = body: may the balance groggy start now?
execute unless score #ph tk matches 1..7 run return fail
execute if score #stag tk matches 1.. run return fail
execute if entity @s[tag=rlk_mb_inv] run return fail
# not in the air patterns (10 공중 장풍, 11 착지 공격: she would hang in the air)
execute if score #pat tk matches 0..9 run return 1
return fail
