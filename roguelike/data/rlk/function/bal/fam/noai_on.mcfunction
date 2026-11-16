# NoAI for the groggy, remembering whether the mob had it before (a freeze that is on holds that in rlk_noai)
execute if score @s frzT matches 1.. if entity @s[tag=rlk_noai] run tag @s add rlk_bal_noai
execute unless score @s frzT matches 1.. if data entity @s {NoAI:1b} run tag @s add rlk_bal_noai
data merge entity @s {NoAI:1b}
