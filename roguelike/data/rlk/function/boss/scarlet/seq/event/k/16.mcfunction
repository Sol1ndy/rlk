# event at #sq 16 (@s = the body).
execute if score #hrEv hr matches 2 run function rlk:boss/scarlet/rig/anchor/hand_l
execute if score #hrEv hr matches 2 at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/ev_palm
