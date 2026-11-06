# event at #sq 30 (@s = the body).
execute if score #hrEv hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_ev_sword]
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/anchor/hand_r
execute if score #hrEv hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s rotated ~ 0 positioned ^-0.02 ^0.02 ^0.04 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_ev","rlk_hr_ev_sword"],item:{id:"minecraft:iron_sword",count:1,components:{"minecraft:item_model":"rlk:mboss/scarlet/item_sword"}},item_display:"none",billboard:"fixed",teleport_duration:1,interpolation_duration:1,view_range:2f,brightness:{block:13,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0.31599f,0.13089f,-0.3596f,0.86816f],scale:[1.375f,1.375f,1.375f],right_rotation:[0f,0f,0f,1f]}}
execute if score #hrEv hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #hrEv hr matches 1 store result score #sq_x0 hr run data get entity @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] Pos[0] 1000
execute if score #hrEv hr matches 1 store result score #sq_y0 hr run data get entity @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] Pos[1] 1000
execute if score #hrEv hr matches 1 store result score #sq_z0 hr run data get entity @e[type=minecraft:item_display,tag=rlk_hr_ev_sword,limit=1] Pos[2] 1000
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_toss
execute if score #hrEv hr matches 2 run kill @e[type=minecraft:marker,tag=rlk_hr_ev_orb]
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/rig/anchor/hand_l
execute if score #hrEv hr matches 2 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] positioned ~ ~0.1 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_ev","rlk_hr_ev_orb"]}
execute if score #hrEv hr matches 2 store result score #sq_x0 hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_ev_orb,limit=1] Pos[0] 1000
execute if score #hrEv hr matches 2 store result score #sq_y0 hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_ev_orb,limit=1] Pos[1] 1000
execute if score #hrEv hr matches 2 store result score #sq_z0 hr run data get entity @e[type=minecraft:marker,tag=rlk_hr_ev_orb,limit=1] Pos[2] 1000
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/fx/snd/ev_toss
