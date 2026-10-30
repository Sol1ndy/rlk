# Fallback 2: 2 b in front of the player's last safe footing (rlk_safe), facing as the player.
execute at @e[tag=rlk_safe,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ^ ^ ^2 run function rlk:room/rift/spot/accept {way:3}
