# The predictive lock (lead 15) re-tagged as the centre; moving player: 2 b further along the velocity.
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:15}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p41c]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p41c
tag @e[type=minecraft:marker,tag=rlk_mb_az_p41c] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p41c] add rlk_mb_az_p41
tag @e[type=minecraft:marker,tag=rlk_mb_az_p41c] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p41c] remove rlk_mb_lock
execute if score #mbV mb matches 81.. as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] at @s if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-2
execute unless score #mbV mb matches 81.. as @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run function rlk:boss/azhdaha/p/frost/c_still
