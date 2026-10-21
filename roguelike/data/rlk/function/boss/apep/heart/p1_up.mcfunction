# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# E t70 (and seq/entrance/done, idempotent): the Heart drawn up into the canopy (30 t, as heart_up). Until the core
# ticks the org objects outside phase 2 (RREV-1) this is one client interpolation per display to the canopy pose
# (om/heart/spawn/canopy's transforms); without a Heart (reload, the test skips) the canopy state at once.
execute unless entity 524c4b4d-4150-4800-8000-000000000000 run return run function rlk:boss/apep/heart/p1_respawn
execute as 524c4b4d-4150-4800-8000-000000000000 if entity @s[tag=rlk_mb_ap_hup] run return 0
data merge entity 524c4b4d-4150-4800-8000-000000000000 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,21.12f,0f],left_rotation:[-0.70711f,0f,0f,0.70711f],scale:[0.84f,0.84f,0.84f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000009 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,21.12f,0f],left_rotation:[-0.65328f,-0.2706f,0.2706f,0.65328f],scale:[0.84f,0.84f,0.84f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000001 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,-3.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000002 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,-2.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000003 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,-2.7f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000004 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,22.36f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.8f,1.8f,1.8f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000005 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[4.6f,27.5f,2.2f],left_rotation:[0.20369f,-0.08364f,-0.37053f,0.90234f],scale:[4.4f,0.9086f,4.4f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000006 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[3.7875f,26.6775f,1.65f],left_rotation:[0.16002f,-0.06263f,-0.35902f,0.91737f],scale:[4.4f,1.15285f,4.4f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000007 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[2.75f,25.555f,1.1f],left_rotation:[0.13115f,-0.0498f,-0.35151f,0.92561f],scale:[4.4f,1.40507f,4.4f],right_rotation:[0f,0f,0f,1f]}}
data merge entity 524c4b4d-4150-4800-8000-000000000008 {start_interpolation:0,interpolation_duration:30,transformation:{translation:[1.4875f,24.1325f,0.55f],left_rotation:[0.11086f,-0.04124f,-0.34623f,0.93066f],scale:[4.4f,1.66164f,4.4f],right_rotation:[0f,0f,0f,1f]}}
tag 524c4b4d-4150-4800-8000-000000000000 add rlk_mb_ap_hup
