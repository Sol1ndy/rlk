# BLUE probe at the locked spot (once): the cap = the steps so far + 4, at most 18.
scoreboard players operation #t hr = #t2 hr
scoreboard players add #t hr 4
execute if score #t hr matches 19.. run scoreboard players set #t hr 18
tag @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] add rlk_hr_a9p
