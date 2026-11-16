# @s = an orb prop: the ribbon at its centre height.
execute if score @s azS matches 1 positioned ~ ~3.6 ~ run function rlk:boss/azhdaha/fx/p/orb_ribbon
execute unless score @s azS matches 1 positioned ~ ~1.1 ~ run function rlk:boss/azhdaha/fx/p/orb_ribbon
