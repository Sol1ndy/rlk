# $(a) bearing, $(r) radius (blocks): one heal orb there, on the floor of the arena (as the arena marker).
$execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ rotated $(a) 0 positioned ^ ^ ^$(r) run function rlk:boss/arlecchino/bond/orb_one
