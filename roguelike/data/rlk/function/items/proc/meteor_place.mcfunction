execute rotated ~ 0 positioned ^ ^ ^6 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_meteor","rlk_isn"]}
scoreboard players set @e[tag=rlk_isn] life 20
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k155 snd matches 1 run function rlk:snd/f164
