# @s = enemy, at @s: the balance breaks — a yellow burst at the head and a shield-break crack
playsound minecraft:item.shield.break hostile @a ~ ~ ~ 1.0 0.7
playsound minecraft:block.anvil.land hostile @a ~ ~ ~ 0.3 1.8
execute if score @s balC matches 1..2 on passengers if entity @s[tag=rlk_hb_bal] at @s run function rlk:bal/fx/burst
execute if score @s balC matches 3 positioned ~ ~2.2 ~ run function rlk:bal/fx/burst
