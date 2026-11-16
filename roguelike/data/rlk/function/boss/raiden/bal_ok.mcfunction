# rlk:bal/boss/ok, as the boss: may the balance groggy start now?
execute unless score @s rdPhase matches 0 run return fail
execute if score @s rdDeath matches 1.. run return fail
execute if score @s rdBlink matches 1.. run return fail
execute if score @s rdPat matches 5 run return fail
execute if score @s rdPat matches 7 run return fail
execute if score @s rdPat matches 98..99 run return fail
execute if score @s rdNext matches 7 run return fail
execute if score @s rdSgEye matches 1.. run return fail
return 1
