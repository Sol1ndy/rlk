# @s = body: may the balance groggy start now? (cruise only)
execute unless score #fgField mb matches 0 run return fail
execute if score #fgSt mb matches 0 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 1 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 2 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 3 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 4 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 5 run return 1
execute if score #fgSt mb matches 1 if score #fgPat mb matches 6 run return 1
return fail
