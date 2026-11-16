# The same element: remaining ticks = max(remaining, 3); a Cryo strike +1 stack (max 3).
execute if score @s azBrT matches ..2 run scoreboard players set @s azBrT 3
execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players add @s azBrS 1
execute if score #azBrIn mb matches 4 if score #azBrStrike mb matches 1 run scoreboard players set #azBrCs mb 1
execute if score @s azBrS matches 4.. run scoreboard players set @s azBrS 3
