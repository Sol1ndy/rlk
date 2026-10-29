scoreboard players set @s cmS 2
scoreboard players set @s cmT 14
function rlk:cm/rv/tgt_kill
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_rv_tgt","rlk_cmlink","rlk_cmsync","rlk_c3new"]}
scoreboard players operation @e[tag=rlk_c3new] cmId = #cid tmp
tag @e[tag=rlk_c3new] remove rlk_c3new
playsound minecraft:entity.phantom.swoop master @a ~ ~ ~ 0.7 1.4
