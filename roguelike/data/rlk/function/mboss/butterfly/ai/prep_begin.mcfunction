# @s = body, butterfly form: the wing element look of #bfPick (1 t switch), the pattern 8 t later; no switch
# needed = at once.
scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 11 run scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 12 run scoreboard players set #bfWant mb 1
execute if score #bfPick mb matches 13 run scoreboard players set #bfWant mb 1
execute if score #bfPick mb matches 14 run scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 15 run scoreboard players set #bfWant mb 7
execute if score #bfLook mb = #bfWant mb run return run function rlk:mboss/butterfly/ai/go
scoreboard players set #bfSt mb 5
scoreboard players set #bfT mb 0
function rlk:mboss/butterfly/look/switch
