# @s = body, pull tick 24: the player 1 b in front of her (floor height, facing her; pull/start t 0 = at once).
# Refused (dead, reviving, selection screen, map view) -> #gp4Ok 0 (the pattern ends at 40). Placed but not
# moved (pull/finish found the destination blocked) -> fizzle, she swings in place.
execute store success score #gp4Ok mb rotated as @s rotated ~ 0 positioned ^ ^ ^1 positioned ~ 201 ~ run function rlk:mboss/pull/start {t:0}
execute if score #gp4Ok mb matches 1 rotated as @s rotated ~ 0 positioned ^ ^ ^1 positioned ~ 201 ~ unless entity @e[tag=rlk_body,distance=..0.6,limit=1] run return run function rlk:mboss/guardian/p/pull/fizzle
execute unless score #gp4Ok mb matches 1 run return run function rlk:mboss/guardian/p/pull/scr_end
scoreboard players set @a[tag=player] vBig 12
title @a[tag=player] times 0 3 0
title @a[tag=player] title [{"text":"\ue514\ue5f0\ue515\ue5f1\ue516\ue5f0\ue517\ue5f0","font":"rlk:mboss_gd","color":"white","shadow_color":0}]
