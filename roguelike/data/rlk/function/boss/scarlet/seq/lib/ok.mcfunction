# At a proposed feet position of a staged move: on the arena floor inside the barrier ring (26.5 b from the axis:
# the walk disc and the ring up to the out-of-bounds line) with free feet and head. The stage axis from the avatar to
# its mv/ok-checked forward point lies inside it, also when the avatar stands outside the safe disc.
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..26.5,limit=1] run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
return 1
