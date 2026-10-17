# Hook aux_hit (@s = a star inside combat/apply, RES already applied to #dmg). Pyro does nothing (immune);
# everything else falls through to the framework default (pool, number, broken tag).
execute if entity @s[tag=rlk_mb_proto_star] if score #elem tmp matches 1 run scoreboard players set #dmg tmp 0
