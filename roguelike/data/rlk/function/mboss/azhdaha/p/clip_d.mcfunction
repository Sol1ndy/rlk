# GENERATED: the running pattern's clip at clock 0 (the core plays it; #azPT = clip tick); variant clips by
# #azPaw / #azSide; clips with a yaw schedule arm the yaw driver.
execute if score #azPat mb matches 1 run return run function rlk:mboss/azhdaha/rig/play/chin_slam
execute if score #azPat mb matches 2 run return run function rlk:mboss/azhdaha/rig/play/jump_slam
execute if score #azPat mb matches 3 run return run function rlk:mboss/azhdaha/rig/play/charge_coil
execute if score #azPat mb matches 4 run return run function rlk:mboss/azhdaha/rig/play/spikes
execute if score #azPat mb matches 5 if score #azPaw mb matches 1 run return run function rlk:mboss/azhdaha/rig/play/stomp_fl
execute if score #azPat mb matches 5 if score #azPaw mb matches 2 run return run function rlk:mboss/azhdaha/rig/play/stomp_fr
execute if score #azPat mb matches 5 if score #azPaw mb matches 3 run return run function rlk:mboss/azhdaha/rig/play/stomp_hl
execute if score #azPat mb matches 5 if score #azPaw mb matches 4 run return run function rlk:mboss/azhdaha/rig/play/stomp_hr
execute if score #azPat mb matches 5 run return run function rlk:mboss/azhdaha/rig/play/stomp_fl
execute if score #azPat mb matches 10 if score #azPaw mb matches 1 run return run function rlk:mboss/azhdaha/rig/play/stomp3_fl
execute if score #azPat mb matches 10 if score #azPaw mb matches 2 run return run function rlk:mboss/azhdaha/rig/play/stomp3_fr
execute if score #azPat mb matches 10 run return run function rlk:mboss/azhdaha/rig/play/stomp3_fl
execute if score #azPat mb matches 6 run return run function rlk:mboss/azhdaha/rig/play/feint
execute if score #azPat mb matches 7 if score #azSide mb matches 1 run return run function rlk:mboss/azhdaha/yaw/play_tail_whip_l
execute if score #azPat mb matches 7 if score #azSide mb matches -1 run return run function rlk:mboss/azhdaha/yaw/play_tail_whip_r
execute if score #azPat mb matches 7 run return run function rlk:mboss/azhdaha/yaw/play_tail_whip_l
execute if score #azPat mb matches 8 run return run function rlk:mboss/azhdaha/rig/play/tail_slam
execute if score #azPat mb matches 9 run return run function rlk:mboss/azhdaha/rig/play/burrow_dive
execute if score #azPat mb matches 43 run return run function rlk:mboss/azhdaha/rig/play/tail_cast
execute if score #azPat mb matches 44 run return run function rlk:mboss/azhdaha/rig/play/tail_cast
execute if score #azPat mb matches 45 run return run function rlk:mboss/azhdaha/rig/play/spikes
execute if score #azPat mb matches 46 run return run function rlk:mboss/azhdaha/rig/play/spikes
execute if score #azPat mb matches 21 run return run function rlk:mboss/azhdaha/rig/play/absorb
execute if score #azPat mb matches 22 run return run function rlk:mboss/azhdaha/rig/play/absorb_p3
execute if score #azPat mb matches 23 run return run function rlk:mboss/azhdaha/rig/play/p3_sink
execute if score #azPat mb matches 28 run return run function rlk:mboss/azhdaha/rig/play/walk
