# Marker rlk_mb_ap_lock on the floor under the player's body, pulled inside the walk disc (any executor).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_lock"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run function rlk:mboss/apep/u/clamp_walk
