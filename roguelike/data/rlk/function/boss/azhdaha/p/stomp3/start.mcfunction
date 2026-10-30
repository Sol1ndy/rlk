# 산명곡응 – 연속 발구르기 (stomp3, id 10) - start (#azPT 0; stomp3_<paw A> by #azPaw: 1 fl, 2 fr)
scoreboard players operation #aq10P mb = #azPaw mb
execute unless score #aq10P mb matches 1..2 run scoreboard players set #aq10P mb 1
kill @e[tag=rlk_mb_az_p10m]
execute if score #aq10P mb matches 1 positioned ^3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s1"]}
execute if score #aq10P mb matches 1 positioned ^-3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s2"]}
execute if score #aq10P mb matches 1 positioned ^3.3 ^0 ^2.5 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s3"]}
execute if score #aq10P mb matches 2 positioned ^-3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s1"]}
execute if score #aq10P mb matches 2 positioned ^3.3 ^0 ^2.55 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s2"]}
execute if score #aq10P mb matches 2 positioned ^-3.3 ^0 ^2.5 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p10","rlk_mb_az_p10m","rlk_mb_az_p10s3"]}
