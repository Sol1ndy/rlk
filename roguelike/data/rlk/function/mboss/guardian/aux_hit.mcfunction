# Hook aux_hit (@s = a star inside combat/apply; #dmg already modified like a body hit, RES included:
# inert stars carry mres 80). Outside a running chaos timer the star takes nothing (no number);
# an active star is immune to its own element (framework "면역" popup when #dmg is 0).
execute unless score #mbSt mb matches 1 run return run function rlk:mboss/guardian/star/ignore
execute unless score #gdSt mb matches 4 run return run function rlk:mboss/guardian/star/ignore
execute unless score #gdCP mb matches 3 run return run function rlk:mboss/guardian/star/ignore
execute unless entity @s[tag=rlk_mb_gd_star] run return 0
execute if score @s mbS matches 1..4 if score #elem tmp = @s mbS run function rlk:mboss/guardian/star/immune
