# Hook cleanup (no executor; idempotent): the barrier walls (recorded blocks) first, then every module entity
# (organisms and their models, the Heart, domes, walls, stalks, the seed, pattern entities, locks, the arena props),
# the stage, the module fake players and storage, the kit's cards and HUD.
function rlk:mboss/apep/wall/clear
function rlk:mboss/apep/org/clear
function rlk:mboss/apep/rev/clear
function rlk:mboss/apep/dome/clear
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
kill @e[tag=rlk_mb_ar_ap_oasis]
kill @e[type=minecraft:husk,tag=rlk_mb_ap_org]
function rlk:mboss/apep/ai/vars
data remove storage rlk:mboss ap
function rlk:mboss/apep/fx/clear
function rlk:mboss/apep/fx/hud/clear
function rlk:mboss/apep/fx/dress/clear
