# The gauge + 1 per hit of hers that landed (#hpp), at most 50 (hr_design §1.2).
scoreboard players operation #t hr = #hpp hr
scoreboard players set #t2 hr 1
scoreboard players operation #t hr *= #t2 hr
scoreboard players operation #gau hr += #t hr
execute if score #gau hr matches 51.. run scoreboard players set #gau hr 50
