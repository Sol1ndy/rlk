# 산명곡응 (stomp, id 5) - start (#azPT 0; the core played stomp_<paw> by #azPaw)
scoreboard players operation #aq5P mb = #azPaw mb
execute unless score #aq5P mb matches 1..4 run scoreboard players set #aq5P mb 1
kill @e[tag=rlk_mb_az_p5m]
execute if score #aq5P mb matches 1 positioned ^3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p5","rlk_mb_az_p5m","rlk_mb_az_p5paw"]}
execute if score #aq5P mb matches 2 positioned ^-3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p5","rlk_mb_az_p5m","rlk_mb_az_p5paw"]}
execute if score #aq5P mb matches 3 positioned ^2.55 ^0 ^-2.85 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p5","rlk_mb_az_p5m","rlk_mb_az_p5paw"]}
execute if score #aq5P mb matches 4 positioned ^-2.55 ^0 ^-2.85 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p5","rlk_mb_az_p5m","rlk_mb_az_p5paw"]}
