# Hook cleanup (no executor; idempotent): module fake players to their defaults, the module storage, the brand
# and the shards, every module entity (props, seal, pattern entities: all rlk_mb_aux, the framework kills them
# too), the kit's cards and HUD flags. The rolled pair survives in cprep.azhdaha.pair (the framework's).
function rlk:mboss/azhdaha/brand/clear_all
function rlk:mboss/azhdaha/ai/vars
kill @e[tag=rlk_mb_az_ap]
kill @e[tag=rlk_mb_az_seal]
kill @e[tag=rlk_mb_az_pat]
kill @e[type=minecraft:marker,tag=rlk_mb_az_kept]
data remove storage rlk:mboss az
function rlk:mboss/azhdaha/kstub/clear
function rlk:mboss/azhdaha/kstub/hud/clear
