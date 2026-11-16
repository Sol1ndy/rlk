# @s = groggy enemy (combat/apply_mods, before the boss incoming hooks and their HP floors): #dmg x the tier %
execute if score @s balC matches 1 run scoreboard players operation #a bal = #amp1 bal
execute if score @s balC matches 2 run scoreboard players operation #a bal = #amp2 bal
execute if score @s balC matches 3 run scoreboard players operation #a bal = #amp3 bal
scoreboard players operation #dmg tmp *= #a bal
scoreboard players operation #dmg tmp /= #100 bal
