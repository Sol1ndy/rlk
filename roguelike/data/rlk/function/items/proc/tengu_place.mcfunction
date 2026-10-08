summon minecraft:marker ~ ~ ~ {Tags:["rlk_tengu","rlk_isn"]}
scoreboard players set @e[tag=rlk_isn] life 30
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:entity.parrot.fly master @a ~ ~ ~ 0.8 0.6
