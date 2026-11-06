# @s = a proxy tagged rlk_hit (a §16 line in char/arlecchino/skill_hit, after the damage): the rest of that skill's
# target-side writes (arDir, the blood-debt mark) go to the body, once per boss, not to each proxy that was in range.
tag @s remove rlk_hit
tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_hit
