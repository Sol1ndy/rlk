# sl 모습 한 틱 (@s = 두뇌, at @s; #cid = cmId). 내 뿌리 부품을 찾고, 나머지 부품은 뿌리와 같은 자리(모두 함께 옮김)에서만 찾음. 자세는 바뀔 때만 보냄(보간)
execute as @e[tag=rlk_c2root,tag=rlk_sl_pt,tag=!rlk_c2dying,distance=..6] if score @s cmId = #cid tmp run tag @s add rlk_c2this
execute at @e[tag=rlk_c2this,limit=1] as @e[tag=rlk_sl_pt,tag=!rlk_c2root,tag=!rlk_c2dying,distance=..0.01] if score @s cmId = #cid tmp run tag @s add rlk_c2this
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 48.. run function rlk:cm/sl/rig/check
tag @e[tag=rlk_c2this] add rlk_cmsync
execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2this] run tp @s ~ ~ ~ ~ 0
execute if score @s cmAH matches 1 as @e[tag=rlk_c2this] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s c2Age matches 2 as @e[tag=rlk_c2this,tag=rlk_c2root] run scoreboard players operation @s mlv = #clv tmp
execute if score @s frzT matches 1.. run return run function rlk:cm/c2/rig_frozen
function rlk:cm/sl/rig/pick
execute unless score @s cmAP = #pose tmp store result storage rlk:c2 p.n int 1 run scoreboard players get #pose tmp
execute unless score @s cmAP = #pose tmp run function rlk:cm/sl/rig/pose_m with storage rlk:c2 p
scoreboard players operation @s cmAP = #pose tmp
execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_c2this] remove rlk_c2this
