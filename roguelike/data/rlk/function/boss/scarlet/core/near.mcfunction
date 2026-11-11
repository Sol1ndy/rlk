# {d,t} Glide (@s = the body, facing the lock marker) in t ticks to the point d blocks before the locked spot on her
# side, on the floor (round V: she never lands on / dashes through the player's spot); a point that fails mv/ok: the
# locked spot itself (core/clamp made it safe).
$execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:$(t)}
$execute positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:$(t)}
