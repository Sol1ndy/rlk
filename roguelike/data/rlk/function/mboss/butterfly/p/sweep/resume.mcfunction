# The fight runs again (@s = body, before this tick's hz/all): every live trail segment gets its red ember line
# back, alive up to its flare (the ticks left + 1).
execute as @e[type=minecraft:marker,tag=rlk_mb_hzq,scores={mbHzV=131}] if score @s mbHzT < @s mbHzW at @s rotated as @s rotated ~ 0 positioned ~ ~0.05 ~ run function rlk:mboss/butterfly/p/sweep/ember
