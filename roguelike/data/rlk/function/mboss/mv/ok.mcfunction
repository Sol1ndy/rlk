# At a proposed feet position: inside the fight arena's safe disc (safe - 0.5 b from the axis) with free feet and head.
# A chapter arena (#mbAr >= 1) through F:mboss/ar/<aid>/ok; the plaza's lines (the M0 text, = ar/plaza/ok) follow inline.
execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/ok
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..18.5,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
