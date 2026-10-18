# STUB rig (tools/mboss_butterfly/stub_rig.py): replaced by the real rig at merge time.
# Body parts back (wings per the form).
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_body,tag=rlk_mb_bfs,limit=1] {start_interpolation:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.7f,2.6f,0.45f]}}
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_bf_head,tag=rlk_mb_bfs,limit=1] {start_interpolation:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.42f,0.42f,0.42f]}}
execute if score @s bfStubF matches 2 run function rlk:mboss/butterfly/rig_stub/form/butterfly
