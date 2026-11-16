# event: the timeline at #sq 43 (@s = the body).
execute if score #hrEv hr matches 1 at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^1.1 ^0.9 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute if score #hrEv hr matches 1 store result score #sq_x hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] 1000
execute if score #hrEv hr matches 1 store result score #sq_y hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] 1000
execute if score #hrEv hr matches 1 store result score #sq_z hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] 1000
execute if score #hrEv hr matches 1 run scoreboard players set #sq_k hr 13
execute if score #hrEv hr matches 1 run scoreboard players set #sq_n hr 14
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_x hr -= #sq_x0 hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_x hr *= #sq_k hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_x hr /= #sq_n hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_x hr += #sq_x0 hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_y hr -= #sq_y0 hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_y hr *= #sq_k hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_y hr /= #sq_n hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_y hr += #sq_y0 hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_z hr -= #sq_z0 hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_z hr *= #sq_k hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_z hr /= #sq_n hr
execute if score #hrEv hr matches 1 run scoreboard players operation #sq_z hr += #sq_z0 hr
execute if score #hrEv hr matches 1 run scoreboard players add #sq_y hr 318
execute if score #hrEv hr matches 1 if score #sq_y hr matches ..202074 run scoreboard players set #sq_y hr 202075
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] double 0.001 run scoreboard players get #sq_x hr
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] double 0.001 run scoreboard players get #sq_y hr
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] double 0.001 run scoreboard players get #sq_z hr
execute if score #hrEv hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] ~ ~ ~
execute if score #hrEv hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
execute if score #hrEv hr matches 1 run data merge entity @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[-0.91521f,-0.37909f,-0.05231f,0.1263f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
execute if score #hrEv hr matches 1 at @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] run function rlk:boss/scarlet/fx/p/ev_trail
