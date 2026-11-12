# {d,t} Glide (@s = the body, facing the lock marker) in t ticks to the point d blocks before the locked spot on her
# side, on the floor (round V: she never lands on / dashes through the player's spot); round W: nor on the player's
# camera (core/cam_ok); a point that fails: 1.5 b farther back, else the locked spot itself (core/clamp made it safe).
$execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:mboss/mv/glide {t:$(t)}
$execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^$(d) positioned ^ ^ ^1.5 if function rlk:mboss/mv/ok if function rlk:boss/scarlet/core/cam_ok run return run function rlk:mboss/mv/glide {t:$(t)}
$execute positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:$(t)}
