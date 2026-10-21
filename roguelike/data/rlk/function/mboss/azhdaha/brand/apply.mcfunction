# @s = player; #azBrIn = the element, #azBrStrike 1 strike / 0 lingering.
scoreboard players set #azBrNew mb 0
execute if score @s azBrT matches 1.. if score @s azBrE = #azBrIn mb run function rlk:mboss/azhdaha/brand/refresh
execute unless score @s azBrT matches 1.. run function rlk:mboss/azhdaha/brand/new
execute if score @s azBrT matches 1.. unless score @s azBrE = #azBrIn mb run function rlk:mboss/azhdaha/brand/new
scoreboard players set #azHudQ mb 1
# rule 33 (S2-L): a Pyro brand by a strike outside the landslide -> p/firefield/on_brand at the floor point
execute if score #azBrStrike mb matches 1 if score #azBrIn mb matches 1 unless score #azPat mb matches 20 at @s positioned ~ 201 ~ as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/azhdaha/p/firefield/on_brand
