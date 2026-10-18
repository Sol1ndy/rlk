# @s = orb: burst fx on the floor under it, its rings / rig prop and itself removed.
execute positioned ~ 201 ~ rotated ~ 0 run function rlk:mboss/butterfly/fx/p/orb_burst
function rlk:mboss/butterfly/fx/snd/orb_burst
particle minecraft:flash{color:[0.92,0.99,0.85,0.9]} ~ ~0.5 ~ 0 0 0 0 1 force @a[tag=player]
execute if entity @s[tag=rlk_mb_bf_p14o0] run kill @e[tag=rlk_mb_bf_p14r0]
execute if entity @s[tag=rlk_mb_bf_p14o1] run kill @e[tag=rlk_mb_bf_p14r1]
execute if entity @s[tag=rlk_mb_bf_p14o0] run kill @e[tag=rlk_mb_bf_p14v0]
execute if entity @s[tag=rlk_mb_bf_p14o1] run kill @e[tag=rlk_mb_bf_p14v1]
kill @s
