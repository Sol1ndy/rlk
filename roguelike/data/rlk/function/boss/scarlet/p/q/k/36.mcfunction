# Q pattern tick 36
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/p/q/lockp
execute if score #q_hit hr matches 1 at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_on
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ^-0.164 ^3.397 ^0.715 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute if score #q_hit hr matches 1 run function rlk:boss/scarlet/fx/follow_off
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3746f,2.03f,0.6394f],left_rotation:[-0.7553f,-0.2899f,0.2106f,0.5488f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_34] remove rlk_hr_trr
