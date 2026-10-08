kill @e[tag=rlk_storm]
execute rotated ~ 0 positioned ^ ^ ^4.5 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_storm","rlk_isn"]}
scoreboard players operation @e[tag=rlk_isn] life = #stormDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:entity.breeze.inhale master @a ~ ~ ~ 1 0.7
playsound minecraft:item.elytra.flying master @a ~ ~ ~ 0.4 1.4
