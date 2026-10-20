# chin/impact Hydro (plan 4.6; Change note 1: keep, the swirl from the call). As the body at the impact point,
# rotated = the crack line: a random side and distance 5-7 b (local x = perpendicular).
kill @e[type=minecraft:marker,tag=rlk_mb_az_xlg]
execute store result score #axlR mb run random value 0..9
execute if score #axlR mb matches 0 positioned ^5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 1 positioned ^5.5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 2 positioned ^6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 3 positioned ^6.5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 4 positioned ^7 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 5 positioned ^-5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 6 positioned ^-5.5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 7 positioned ^-6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 8 positioned ^-6.5 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute if score #axlR mb matches 9 positioned ^-7 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_x","rlk_mb_az_xlg"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xlg,limit=1] run function rlk:mboss/azhdaha/u/clamp_w
execute at @e[type=minecraft:marker,tag=rlk_mb_az_xlg,limit=1] run function rlk:mboss/azhdaha/xl/chin_impact/hydro_at
kill @e[type=minecraft:marker,tag=rlk_mb_az_xlg]
