# Round 4 markers (#azB3T 309, strike 357): 2 safe circles r 2.8 (safe within R0 + 0.3): both >= 8 b from the emergence spot (the centre),
# one relative to the player (reachable within the 48 t), the rest on rings r 9-16 >= 50 degrees apart;
# then the mask hazard and the safe markers (same tick, cm.md 13.6), the wash and the rims.
kill @e[type=minecraft:marker,tag=rlk_mb_az_p42s]
scoreboard players set #aq42J mb 3
scoreboard players set #aq42S mb 357
scoreboard players set #aq42In mb 0
scoreboard players set #aq42Dp mb -1
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 0
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] at @s run function rlk:mboss/azhdaha/p/bolt/pl_r4
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute store result score #aq42A mb run random value 0..359
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 1
scoreboard players operation #aq42X mb = #aq42A mb
scoreboard players add #aq42X mb 0
execute store result score #aq42Y mb run random value -10..10
scoreboard players operation #aq42X mb += #aq42Y mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] store result entity @s Rotation[0] float 1 run scoreboard players get #aq42X mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] run function rlk:mboss/azhdaha/p/bolt/ring
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/p/bolt/mask_3
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/fx/tele/mask_wash {r:280,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=0},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:0,r:28,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=1},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:1,r:28,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/fx/snd/bolt_marker
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42n] remove rlk_mb_az_p42n
