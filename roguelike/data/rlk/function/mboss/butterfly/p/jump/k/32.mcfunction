# jump clock 32
function rlk:mboss/butterfly/rig/face/track
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p2b]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p2b","rlk_mb_bf_kept"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:25,tell:10,dmg:70}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] run playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.45 1.8 0.15
