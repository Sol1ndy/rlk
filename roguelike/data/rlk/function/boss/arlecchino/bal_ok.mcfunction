# @s = body: may the balance groggy start now?
execute unless score #ph kn matches 1..5 run return fail
execute if entity @s[tag=rlk_kn_win] run return fail
execute if score #stun kn matches 1 run return fail
execute if score #pat kn matches 0 run return 1
execute if score #pat kn matches 1 run return 1
execute if score #pat kn matches 2 run return 1
execute if score #pat kn matches 3 run return 1
execute if score #pat kn matches 4 run return 1
execute if score #pat kn matches 5 run return 1
execute if score #pat kn matches 6 run return 1
execute if score #pat kn matches 7 run return 1
execute if score #pat kn matches 8 run return 1
execute if score #pat kn matches 9 run return 1
execute if score #pat kn matches 11 run return 1
execute if score #pat kn matches 12 run return 1
execute if score #pat kn matches 13 run return 1
execute if score #pat kn matches 41 run return 1
execute if score #pat kn matches 42 run return 1
execute if score #pat kn matches 43 run return 1
execute if score #pat kn matches 44 run return 1
execute if score #pat kn matches 45 run return 1
execute if score #pat kn matches 48 run return 1
return fail
