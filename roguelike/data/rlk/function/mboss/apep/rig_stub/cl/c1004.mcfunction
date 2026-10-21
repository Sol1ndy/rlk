# crawl_p1 (16 t)
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/hand/b_hand_l/p1_curl
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/hand/c_hand_r/p1_curl
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/hand/b_hand_r/p1_open
execute if score @s apRigT matches 0 run function rlk:mboss/apep/rig_stub/hand/c_hand_l/p1_open
execute if score @s apRigT matches 8 run function rlk:mboss/apep/rig_stub/hand/b_hand_l/p1_open
execute if score @s apRigT matches 8 run function rlk:mboss/apep/rig_stub/hand/c_hand_r/p1_open
execute if score @s apRigT matches 8 run function rlk:mboss/apep/rig_stub/hand/b_hand_r/p1_curl
execute if score @s apRigT matches 8 run function rlk:mboss/apep/rig_stub/hand/c_hand_l/p1_curl
execute if score @s apRigT matches 16.. run scoreboard players set @s apRigT 0
