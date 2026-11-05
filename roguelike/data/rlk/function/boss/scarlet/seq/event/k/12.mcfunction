# event at #sq 12 (@s = the body).
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig/anchor/hand_r
execute if score #hrEv hr matches 1 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/ev_glint
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/fx/snd/ev_chime
