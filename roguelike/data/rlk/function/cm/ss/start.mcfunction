scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_ss tmp
scoreboard players operation @s cmCd = #c2Cd_ss tmp
summon minecraft:item_display ~ ~0.06 ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_c2ring","rlk_c2new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:1,view_range:1.5f,width:3.2f,height:0.3f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c2/fx/ring","minecraft:custom_model_data":{colors:[16777215]}}}}
scoreboard players operation @e[tag=rlk_c2new] cmId = @s cmId
tag @e[tag=rlk_c2new] add rlk_cmsync
tag @e[tag=rlk_c2new] remove rlk_c2new
execute unless score #c2sslatch snd matches 1 run function rlk:cm/c2/snd/sslatch
execute unless score #c2sshum snd matches 1 run function rlk:cm/c2/snd/sshum
