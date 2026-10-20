# t26: F1 = lockv (lead 30); F2 = F1 + 5 b along the velocity (a standing player: along the boss -> player line);
# F3 = random 6-10 b from the player; each in the walk disc; the star seals and their hazards.
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
function rlk:mboss/mv/lockv {lead:30}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_az_p45f0]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p45f0
tag @e[type=minecraft:marker,tag=rlk_mb_az_p45f0] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p45f0] add rlk_mb_az_p45
tag @e[type=minecraft:marker,tag=rlk_mb_az_p45f0] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p45f0] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f0,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p45","rlk_mb_az_p45f1"]}
execute if score #mbV mb matches 81.. as @e[type=minecraft:marker,tag=rlk_mb_az_p45f1,limit=1] at @s if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-5
execute unless score #mbV mb matches 81.. as @e[type=minecraft:marker,tag=rlk_mb_az_p45f1,limit=1] at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-5
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p45","rlk_mb_az_p45f2"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45f2,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359
execute store result storage rlk:mboss az.p45.d int 1 run random value 6..10
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45f2,limit=1] at @s rotated as @s run function rlk:mboss/azhdaha/p/icespike/mv with storage rlk:mboss az.p45
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45f0,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f0,limit=1] run function rlk:mboss/azhdaha/p/icespike/f0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45f1,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f1,limit=1] run function rlk:mboss/azhdaha/p/icespike/f1
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p45f2,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p45f2,limit=1] run function rlk:mboss/azhdaha/p/icespike/f2
