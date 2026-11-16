# The silhouette display (scale 8; right_rotation cancels the item renderer's turn, so +Z is her facing).
$summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_move_fx","rlk_rd_mvnew"],billboard:"fixed",item_display:"none",teleport_duration:0,brightness:{block:15,sky:15},shadow_radius:0f,view_range:3f,width:10f,height:8f,transformation:{translation:[0f,0f,0f],scale:[8f,8f,8f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_movement/$(model)"}}}
execute rotated as @s run tp @e[tag=rlk_rd_mvnew] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_mvnew] rdMvAge -1
$scoreboard players set @e[tag=rlk_rd_mvnew] rdMvKind $(kind)
execute if score @s rdPhase matches 2 run tag @e[tag=rlk_rd_mvnew] add rlk_rd_mv_t
tag @e[tag=rlk_rd_mvnew] remove rlk_rd_mvnew
