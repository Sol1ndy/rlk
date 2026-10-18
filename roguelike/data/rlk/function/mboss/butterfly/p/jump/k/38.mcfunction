# jump clock 38
function rlk:mboss/butterfly/rig_stub/face/track
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~-1.32 ~2.05 ~-0.48 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.667f,0.859f,0.518f],scale:1} ~1.32 ~2.05 ~0.48 0 0 0 0 1 force @a[tag=player]
playsound minecraft:entity.breeze.idle_air hostile @a[tag=player] ~ ~ ~ 0.4 0.8 0.13
kill @e[type=minecraft:marker,tag=rlk_mb_bf_p2b]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p2b"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] at @s unless entity @e[tag=rlk_mb_arena,distance=..20.3,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^0.25
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:25,tell:12,dmg:140}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/disc {r:25,tell:12,el:7,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] run function rlk:mboss/butterfly/fx/card {kind:"glint",pos:"~ ~3 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.8,move:"0f,0f,0f",life:12,fade:3,col:15072200}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] run playsound minecraft:block.amethyst_cluster.hit hostile @a[tag=player] ~ ~ ~ 0.45 1.8 0.15
