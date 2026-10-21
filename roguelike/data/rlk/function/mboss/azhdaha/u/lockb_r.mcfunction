# Macro {r}: the lock pulled into the disc r about the arena centre.
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_lock"]}
$execute as @e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1] run function rlk:mboss/azhdaha/u/clamp_r {r:$(r)}
