# Every 4 t (module clock): the rune over the branded player.
scoreboard players operation #azM mb = #azClk mb
scoreboard players operation #azM mb %= #azK4 mb
execute unless score #azM mb matches 0 run return 0
execute if score @s azBrE matches 1 at @s positioned ~ ~1.2 ~ run function rlk:mboss/azhdaha/kstub/p/brand_rune/1
execute if score @s azBrE matches 2 at @s positioned ~ ~1.2 ~ run function rlk:mboss/azhdaha/kstub/p/brand_rune/2
execute if score @s azBrE matches 3 at @s positioned ~ ~1.2 ~ run function rlk:mboss/azhdaha/kstub/p/brand_rune/3
execute if score @s azBrE matches 4 at @s positioned ~ ~1.2 ~ run function rlk:mboss/azhdaha/kstub/p/brand_rune/4
