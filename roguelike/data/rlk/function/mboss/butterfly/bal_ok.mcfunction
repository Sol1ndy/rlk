# @s = body: may the balance groggy start now?
execute if score #bfSt mb matches 0 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 0 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 1 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 2 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 3 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 4 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 11 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 12 run return 1
execute if score #bfSt mb matches 1 if score #bfPat mb matches 13 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 1 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 2 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 3 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 4 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 11 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 12 run return 1
execute if score #bfSt mb matches 2 if score #bfPat mb matches 13 run return 1
return fail
