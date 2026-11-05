# lead_down at #sq 29 (@s = the body).
scoreboard players set #sq_sig hr 4
function rlk:boss/scarlet/fx/snd/shield_refill
execute positioned ~ ~1.4 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/shield_refill
