# At a proposed body position: inside r 16.5 (butterfly form) with free feet and head.
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
