# Form p1: the body models (the player avatar's rlk:player_motion/arle/*), the wings (shown only with look/wings/open), scythe_l hidden. @s = the boss.
scoreboard players set @s knRigForm 0
data modify entity 524c4b4d-4b4e-4100-8000-000000000000 item.components."minecraft:item_model" set value "rlk:player_motion/arle/head"
data modify entity 524c4b4d-4b4e-4100-8000-000000000001 item.components."minecraft:item_model" set value "rlk:player_motion/arle/body"
data modify entity 524c4b4d-4b4e-4100-8000-000000000002 item.components."minecraft:item_model" set value "rlk:player_motion/arle/right_arm"
data modify entity 524c4b4d-4b4e-4100-8000-000000000003 item.components."minecraft:item_model" set value "rlk:player_motion/arle/right_forearm"
data modify entity 524c4b4d-4b4e-4100-8000-000000000004 item.components."minecraft:item_model" set value "rlk:player_motion/arle/left_arm"
data modify entity 524c4b4d-4b4e-4100-8000-000000000005 item.components."minecraft:item_model" set value "rlk:player_motion/arle/left_forearm"
data modify entity 524c4b4d-4b4e-4100-8000-000000000006 item.components."minecraft:item_model" set value "rlk:player_motion/arle/right_leg"
data modify entity 524c4b4d-4b4e-4100-8000-000000000007 item.components."minecraft:item_model" set value "rlk:player_motion/arle/right_shin"
data modify entity 524c4b4d-4b4e-4100-8000-000000000008 item.components."minecraft:item_model" set value "rlk:player_motion/arle/left_leg"
data modify entity 524c4b4d-4b4e-4100-8000-000000000009 item.components."minecraft:item_model" set value "rlk:player_motion/arle/left_shin"
function rlk:boss/arlecchino/rig/look/r/legs
function rlk:boss/arlecchino/rig/look/r/scythe_l
