# five burning feathers: -30 / -15 / 0 / +15 / +30 deg around the line to the chest
execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8 rotated ~-30 ~ run function rlk:cm/rv/fe_new
execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8 rotated ~-15 ~ run function rlk:cm/rv/fe_new
execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8 rotated ~0 ~ run function rlk:cm/rv/fe_new
execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8 rotated ~15 ~ run function rlk:cm/rv/fe_new
execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8 rotated ~30 ~ run function rlk:cm/rv/fe_new
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 1 1.1
playsound minecraft:entity.phantom.flap master @a ~ ~ ~ 1 1.5
scoreboard players set @s cmS 7
scoreboard players set @s cmT 8
tag @s remove rlk_cmch
scoreboard players set @s cmCd 70
