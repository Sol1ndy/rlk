# Round X (x_brief rulings 1-2; tools/mboss_scarlet/body.py): the body rule at the end of a fight tick (@s = the body, at it;
# P1 / P2 / G1 / G2): her glide checked against the live avatar (core/guard), the avatar kept 1.4 b off her (core/sep).
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute if entity @s[tag=rlk_mb_mv] run function rlk:boss/scarlet/core/guard
execute at @s positioned ~ 201 ~ if entity @e[tag=rlk_body,distance=..2.2] run function rlk:boss/scarlet/core/sep
