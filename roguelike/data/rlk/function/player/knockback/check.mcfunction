# At the proposed feet position. Sample every block touched by a 0.6 x 1.8 body.
# Corners cover both horizontal axes; vertical gaps stay below one block.
# A tiny inward margin permits standing exactly against floors and walls.
execute unless block ~-0.2999 ~0.0001 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~-0.2999 ~0.0001 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~0.0001 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~0.0001 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~-0.2999 ~0.9 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~-0.2999 ~0.9 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~0.9 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~0.9 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~-0.2999 ~1.7999 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~-0.2999 ~1.7999 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~1.7999 ~-0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
execute unless block ~0.2999 ~1.7999 ~0.2999 #rlk:dash_pass run scoreboard players set #pkbBlocked tmp 1
