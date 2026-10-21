# Round 1 markers (#azB3T 75, strike 123): 5 safe circles r 3.2 (safe within R0 + 0.3): one on the tail (the anchor),
# one relative to the player (reachable within the 48 t), the rest on rings r 9-16 >= 50 degrees apart;
# then the mask hazard and the safe markers (same tick, cm.md 13.6), the wash and the rims.
kill @e[type=minecraft:marker,tag=rlk_mb_az_p42s]
scoreboard players set #aq42J mb 0
scoreboard players set #aq42S mb 123
scoreboard players set #aq42In mb 0
scoreboard players set #aq42Dp mb -1
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 0
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 1
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] at @s run function rlk:mboss/azhdaha/p/bolt/pl
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute store result score #aq42A mb run random value 0..359
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 2
scoreboard players operation #aq42X mb = #aq42A mb
scoreboard players add #aq42X mb 0
execute store result score #aq42Y mb run random value -10..10
scoreboard players operation #aq42X mb += #aq42Y mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] store result entity @s Rotation[0] float 1 run scoreboard players get #aq42X mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] run function rlk:mboss/azhdaha/p/bolt/ring
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 3
scoreboard players operation #aq42X mb = #aq42A mb
scoreboard players add #aq42X mb 120
execute store result score #aq42Y mb run random value -10..10
scoreboard players operation #aq42X mb += #aq42Y mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] store result entity @s Rotation[0] float 1 run scoreboard players get #aq42X mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] run function rlk:mboss/azhdaha/p/bolt/ring
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p42","rlk_mb_az_p42s","rlk_mb_az_p42n","rlk_mb_az_p42t"]}
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p42t] mbS 4
scoreboard players operation #aq42X mb = #aq42A mb
scoreboard players add #aq42X mb 240
execute store result score #aq42Y mb run random value -10..10
scoreboard players operation #aq42X mb += #aq42Y mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] store result entity @s Rotation[0] float 1 run scoreboard players get #aq42X mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p42t] run function rlk:mboss/azhdaha/p/bolt/ring
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42t] remove rlk_mb_az_p42t
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/p/bolt/mask_0
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/fx/tele/mask_wash {r:280,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=0},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:0,r:32,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=1},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:1,r:32,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=2},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:2,r:32,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=3},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:3,r:32,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42n,scores={mbS=4},limit=1] run function rlk:mboss/azhdaha/fx/tele/safe_rim {id:4,r:32,tell:48,hold:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/azhdaha/fx/snd/bolt_marker
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42n] remove rlk_mb_az_p42n
