# STUB rig (tools/mboss_fieldgen/stub_rig.py): replaced by the real rig (wip/fg-rig) at merge time.
# Every visible part at scale 0 (the warp).
scoreboard players set @s fgRigV 1
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_ring,tag=rlk_mb_fgs,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_core,tag=rlk_mb_fgs,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_halo,tag=rlk_mb_fgs,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_fg_pend,tag=rlk_mb_fgs,limit=1] {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
