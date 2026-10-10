kill @e[tag=rlk_storm]
execute rotated ~ 0 positioned ^ ^ ^4.5 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_storm","rlk_isn"]}
scoreboard players operation @e[tag=rlk_isn] life = #stormDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k172 snd matches 1 run function rlk:snd/f183
execute unless score #k173 snd matches 1 run function rlk:snd/f184
