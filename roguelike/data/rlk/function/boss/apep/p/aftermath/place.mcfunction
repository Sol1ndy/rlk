# @s = body (B0): the three footprints from the player's bearing about the centre (plan 7.8), on the floor.
kill @e[tag=rlk_mb_ap_p32f]
execute positioned 440 201 8 facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/apep/p/aftermath/place_t
