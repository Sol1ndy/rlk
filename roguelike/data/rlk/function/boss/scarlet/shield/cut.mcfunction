# {s}: a counting cut (@s / position = its marker at the lock point; S4 g/cut/lock): the pip window of strike tick s on
# the gauntlet clock #pt hr, at this lock point (a marker rlk_hr_pip, objective hr = s).
execute if entity @s[tag=rlk_hr_cut] at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_pip","rlk_hr_pipnew"]}
execute unless entity @s[tag=rlk_hr_cut] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_pip","rlk_hr_pipnew"]}
$scoreboard players set @e[type=minecraft:marker,tag=rlk_hr_pipnew] hr $(s)
tag @e[type=minecraft:marker,tag=rlk_hr_pipnew] remove rlk_hr_pipnew
