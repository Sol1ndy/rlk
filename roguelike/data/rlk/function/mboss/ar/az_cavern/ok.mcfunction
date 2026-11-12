# At a proposed feet position: inside the safe disc of az_cavern (25.5 b from the axis) with free feet and head.
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..25.5,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
