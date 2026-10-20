# 72: a shard now (cooldown ignored; the brand element, else the leg element).
kill @e[type=minecraft:item_display,tag=rlk_az_shard]
scoreboard players set #azShCd mb 0
execute as @a[tag=player,limit=1] unless score @s azBrT matches 1.. run scoreboard players operation @s azBrE = #azLeg mb
execute as @a[tag=player,limit=1] run function rlk:mboss/azhdaha/brand/shard_try
