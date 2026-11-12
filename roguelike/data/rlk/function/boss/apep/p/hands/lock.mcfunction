# @s = body (t33): the lock (lead 6) kept as rlk_mb_ap_p2k; the four stalk roots.
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
function rlk:mboss/mv/lockv {lead:6}
tag @e[type=minecraft:marker,tag=rlk_mb_lock] add rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] remove rlk_mb_lock
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p2k]
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_kept
tag @e[type=minecraft:marker,tag=rlk_mb_ap_lock] add rlk_mb_ap_p2k
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p2k] remove rlk_mb_ap_lock
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p2k] remove rlk_mb_lock
# stalk 0 (near right, slam 1 at t62): 6.6 b from the lock at +60 deg of the lock -> boss
# direction, facing the lock; a root beyond the walk disc steps toward the lock (0.5 b, at least 2.5 b off it).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~60 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p2","rlk_mb_ap_p2s0"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~60 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #apq2N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s0,limit=1] at @s run function rlk:boss/apep/p/hands/root
# stalk 1 (far left, slam 2 at t69): 6.6 b from the lock at -140 deg of the lock -> boss
# direction, facing the lock; a root beyond the walk disc steps toward the lock (0.5 b, at least 2.5 b off it).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~-140 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p2","rlk_mb_ap_p2s1"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~-140 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #apq2N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s1,limit=1] at @s run function rlk:boss/apep/p/hands/root
# stalk 2 (near left, slam 3 at t75): 6.6 b from the lock at -60 deg of the lock -> boss
# direction, facing the lock; a root beyond the walk disc steps toward the lock (0.5 b, at least 2.5 b off it).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~-60 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p2","rlk_mb_ap_p2s2"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~-60 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #apq2N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s2,limit=1] at @s run function rlk:boss/apep/p/hands/root
# stalk 3 (far right, slam 4 at t82): 6.6 b from the lock at +140 deg of the lock -> boss
# direction, facing the lock; a root beyond the walk disc steps toward the lock (0.5 b, at least 2.5 b off it).
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3]
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~140 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p2","rlk_mb_ap_p2s3"]}
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] facing entity @s feet rotated ~140 0 positioned ^ ^ ^6.6 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] ~ ~ ~ ~ 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_p2k,limit=1] feet run tp @s ~ ~ ~ ~ 0
scoreboard players set #apq2N mb 0
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p2s3,limit=1] at @s run function rlk:boss/apep/p/hands/root
