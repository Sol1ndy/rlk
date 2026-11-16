# Marker rlk_mb_bf_lock on the floor under the player's body, pulled inside the safe disc (any executor).
kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_lock"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_lock,limit=1] run function rlk:mboss/mv/clamp
