# Hook uninstall (no executor; every enabled module): the rig (real or stand-in), the kit, the module entities,
# objectives and storage.
function rlk:boss/apep/rig/kill
function rlk:boss/apep/rig/uninstall
function rlk:boss/apep/fx/uninstall
function rlk:boss/apep/wall/clear
kill @e[tag=rlk_mb_ap_pat]
kill @e[tag=rlk_mb_ap_kept]
kill @e[tag=rlk_mb_ap_lock]
kill @e[tag=rlk_mb_ap_pop]
kill @e[tag=rlk_mb_ap_heart]
kill @e[tag=rlk_mb_ap_heartd]
kill @e[tag=rlk_mb_ap_dome]
kill @e[tag=rlk_mb_ap_domed]
kill @e[tag=rlk_mb_ap_wall]
kill @e[tag=rlk_mb_ap_wall_blade]
kill @e[tag=rlk_mb_ap_stalk]
kill @e[tag=rlk_mb_ap_stalkd]
kill @e[tag=rlk_mb_ap_seed]
kill @e[tag=rlk_mb_ap_om]
kill @e[tag=rlk_mb_ap_aft]
kill @e[tag=rlk_mb_ap_burstq]
kill @e[tag=rlk_mb_ar_ap_oasis]
kill @e[type=minecraft:husk,tag=rlk_mb_ap_org]
# every AP-ORG display (organism models, the Heart, domes, stalks, the seed, wall
# blades; AP-I2 RREV-4): their husks die above, so the dismounted models go by tag
kill @e[tag=rlk_ap_om]
kill @e[tag=rlk_mb_ap_gate]
data remove storage rlk:mboss ap
scoreboard objectives remove apK
scoreboard objectives remove apS
scoreboard objectives remove apT
scoreboard objectives remove apL
scoreboard objectives remove apShd
scoreboard objectives remove apOC
scoreboard objectives remove apOI
scoreboard objectives remove apSock
scoreboard objectives remove apTok
