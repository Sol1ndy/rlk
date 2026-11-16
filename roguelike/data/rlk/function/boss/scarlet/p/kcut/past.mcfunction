# KCUT probe at the locked spot (once): the cap = the steps so far + 6, at most 20.
scoreboard players operation #t hr = #t2 hr
scoreboard players add #t hr 6
execute if score #t hr matches 21.. run scoreboard players set #t hr 20
tag @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] add rlk_hr_a9p
