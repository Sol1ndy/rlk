# One display per fixed hazard origin; all geometry is in its local coordinates.
# Native ItemDisplayRenderer applies Y=180deg after display transformations.
# Right-rotate 180deg to cancel that item-only flip: mesh +Z now equals ^ ^ ^forward.
scoreboard players add #rdHazardSerial rd 1
scoreboard players operation @s rdHId = #rdHazardSerial rd
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_hvfx","rlk_rd_vnew","rlk_raiden_aux","rlk_room"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:0,teleport_duration:0,view_range:3f,width:48f,height:22f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[32f,32f,32f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/warning_1"}}}
data modify entity @e[tag=rlk_rd_vnew,limit=1] Rotation set from entity @s Rotation
scoreboard players operation @e[tag=rlk_rd_vnew,limit=1] rdVId = @s rdHId
scoreboard players operation @e[tag=rlk_rd_vnew,limit=1] rdShape = @s rdShape
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdWind 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHAge 0
execute as @e[tag=rlk_rd_vnew,limit=1] run function rlk:boss/raiden/hazard/vfx_warning
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
