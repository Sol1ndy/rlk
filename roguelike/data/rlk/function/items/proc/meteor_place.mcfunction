execute rotated ~ 0 positioned ^ ^ ^6 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_meteor","rlk_isn"]}
scoreboard players set @e[tag=rlk_isn] life 20
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:entity.wither.shoot master @a ~ ~ ~ 0.5 0.5
