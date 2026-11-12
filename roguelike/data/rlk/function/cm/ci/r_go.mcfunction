# lock the ram line now: from its centre to the chest
execute positioned ~ ~0.45 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ~ ~-0.45 ~ run tp @s ~ ~ ~ ~ ~
scoreboard players set @s cmS 2
scoreboard players set @s cmT 12
playsound minecraft:entity.breeze.shoot master @a ~ ~ ~ 0.8 1.6
