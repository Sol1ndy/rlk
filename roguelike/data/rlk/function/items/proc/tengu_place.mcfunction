summon minecraft:marker ~ ~ ~ {Tags:["rlk_tengu","rlk_isn"]}
scoreboard players set @e[tag=rlk_isn] life 30
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k157 snd matches 1 run function rlk:snd/f166
