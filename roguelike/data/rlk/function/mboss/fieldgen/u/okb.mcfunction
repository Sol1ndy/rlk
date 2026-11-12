# At a proposed body position: mv/ok (free, inside the safe disc) and within the body disc r 16.5.
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] run return fail
execute unless function rlk:mboss/mv/ok run return fail
return 1
