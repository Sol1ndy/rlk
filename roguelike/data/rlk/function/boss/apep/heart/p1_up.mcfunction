# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# E t70 (and seq/entrance/done, idempotent): the Heart drawn up into the canopy (heart_up, 30 t, then the
# heart_hang sway; the core steps the clips: obj/tick); without a Heart (reload, the test skips) the canopy
# state at once.
execute unless entity 524c4b4d-4150-4800-8000-000000000000 run return run function rlk:boss/apep/heart/p1_respawn
execute as 524c4b4d-4150-4800-8000-000000000000 if entity @s[tag=rlk_mb_ap_hup] run return 0
function rlk:boss/apep/om/heart/play/heart_up
tag 524c4b4d-4150-4800-8000-000000000000 add rlk_mb_ap_hup
