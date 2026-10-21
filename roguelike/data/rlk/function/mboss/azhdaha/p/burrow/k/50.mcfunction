# burrow #azPT 50
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:6}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p9r1]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_kept
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p9r1
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9r1] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p9r1] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p9r1,limit=1] run function rlk:mboss/azhdaha/p/burrow/ring_at
execute if score #mbV mb matches 81.. at @e[type=minecraft:marker,tag=rlk_mb_az_p9r1,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:mboss/azhdaha/p/burrow/rocks_at
execute unless score #mbV mb matches 81.. at @e[type=minecraft:marker,tag=rlk_mb_az_p9r1,limit=1] facing entity @s feet rotated ~180 0 run function rlk:mboss/azhdaha/p/burrow/rocks_at
