# The wall cast (O4): nest_cast; the spots are locked now at the player's feet and facing (no decal: the loop pose is the
# tell, plan 14); 30 %: one arc ahead of the player instead of three groups round them.
scoreboard players set @s apS 2
scoreboard players set @s apT 0
function rlk:boss/apep/om/nest/play/nest_cast
kill @e[type=minecraft:marker,tag=rlk_mb_ap_new]
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_wlock","rlk_mb_ap_new"]}
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_mb_ap_new,limit=1] run tp @s ~ 201 ~ ~ 0
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = @s apL
execute store result score #apR mb run random value 0..99
execute if score #apR mb matches ..29 run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS 1
execute if score #apR mb matches 30.. run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS 0
tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new
