# The gauge + 3 when a pattern ends (not A6, not U), at most 50.
scoreboard players add #gau hr 3
execute if score #gau hr matches 51.. run scoreboard players set #gau hr 50
