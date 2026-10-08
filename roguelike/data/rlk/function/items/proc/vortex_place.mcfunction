kill @e[tag=rlk_vortex]
execute rotated ~ 0 positioned ^ ^ ^3.5 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_vortex","rlk_isn"]}
scoreboard players operation @e[tag=rlk_isn] life = #vortexDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:entity.breeze.inhale master @a ~ ~ ~ 0.9 1.0
