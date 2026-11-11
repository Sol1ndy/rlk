# event: the timeline at #sq 32 (@s = the body).
execute if score #hrEv hr matches 1 as @e[type=minecraft:text_display,tag=rlk_mb_camt] run data merge entity @s {text:{text:"그 검의 주",color:"#F2D0E8"},background:-1207959552}
execute if score #hrEv hr matches 1 if entity @a[tag=player,tag=rlk_mb_camh] as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #hrEv hr matches 1 at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^1.1 ^0.9 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute if score #hrEv hr matches 1 store result score #sq_x hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] 1000
execute if score #hrEv hr matches 1 store result score #sq_y hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] 1000
execute if score #hrEv hr matches 1 store result score #sq_z hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] 1000
execute if score #hrEv hr matches 1 run scoreboard players set #sq_k hr 2
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
execute if score #hrEv hr matches 1 run scoreboard players add #sq_y hr 588
execute if score #hrEv hr matches 1 if score #sq_y hr matches ..202074 run scoreboard players set #sq_y hr 202075
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] double 0.001 run scoreboard players get #sq_x hr
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] double 0.001 run scoreboard players get #sq_y hr
execute if score #hrEv hr matches 1 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] double 0.001 run scoreboard players get #sq_z hr
execute if score #hrEv hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] ~ ~ ~
execute if score #hrEv hr matches 1 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
execute if score #hrEv hr matches 1 run data merge entity @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0.06904f,0.0286f,-0.38161f,0.9213f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
execute if score #hrEv hr matches 1 at @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] run function rlk:boss/scarlet/fx/p/ev_trail
execute if score #hrEv hr matches 2 at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqh"]}
execute if score #hrEv hr matches 2 store result score #sq_x hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] 1000
execute if score #hrEv hr matches 2 store result score #sq_y hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] 1000
execute if score #hrEv hr matches 2 store result score #sq_z hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] 1000
execute if score #hrEv hr matches 2 run scoreboard players set #sq_k hr 2
execute if score #hrEv hr matches 2 run scoreboard players set #sq_n hr 12
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_x hr -= #sq_x0 hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_x hr *= #sq_k hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_x hr /= #sq_n hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_x hr += #sq_x0 hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_y hr -= #sq_y0 hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_y hr *= #sq_k hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_y hr /= #sq_n hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_y hr += #sq_y0 hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_z hr -= #sq_z0 hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_z hr *= #sq_k hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_z hr /= #sq_n hr
execute if score #hrEv hr matches 2 run scoreboard players operation #sq_z hr += #sq_z0 hr
execute if score #hrEv hr matches 2 run scoreboard players add #sq_y hr 167
execute if score #hrEv hr matches 2 if score #sq_y hr matches ..201999 run scoreboard players set #sq_y hr 202000
execute if score #hrEv hr matches 2 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[0] double 0.001 run scoreboard players get #sq_x hr
execute if score #hrEv hr matches 2 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[1] double 0.001 run scoreboard players get #sq_y hr
execute if score #hrEv hr matches 2 store result entity @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] Pos[2] double 0.001 run scoreboard players get #sq_z hr
execute if score #hrEv hr matches 2 at @e[type=minecraft:marker,tag=rlk_hr_sqh,limit=1] run tp @e[type=minecraft:marker,tag=rlk_hr_ev_orb,limit=1] ~ ~ ~
execute if score #hrEv hr matches 2 run kill @e[type=minecraft:marker,tag=rlk_hr_sqh]
execute if score #hrEv hr matches 2 at @e[type=minecraft:marker,tag=rlk_hr_ev_orb,limit=1] run function rlk:boss/scarlet/fx/p/ev_palm
