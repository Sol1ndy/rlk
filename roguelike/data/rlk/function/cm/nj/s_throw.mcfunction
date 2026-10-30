# three shuriken, -15 / 0 / +15 deg around the line to the chest
execute positioned ~ ~1.3 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.6 rotated ~-15 ~ run function rlk:cm/nj/shu_new
execute positioned ~ ~1.3 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.6 run function rlk:cm/nj/shu_new
execute positioned ~ ~1.3 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.6 rotated ~15 ~ run function rlk:cm/nj/shu_new
playsound minecraft:item.trident.throw master @a ~ ~ ~ 1 1.6
scoreboard players set @s cmS 6
scoreboard players set @s cmT 6
scoreboard players set @s cmCd2 60
