# Hook uninstall (no executor; every enabled module): the rig (real or stand-in), the kit, the module
# entities, objectives and storage; the entrance glow chain.
function rlk:boss/azhdaha/rig/kill
function rlk:boss/azhdaha/rig/uninstall
function rlk:boss/azhdaha/fx/uninstall
kill @e[tag=rlk_mb_az_ap]
kill @e[tag=rlk_mb_az_seal]
kill @e[tag=rlk_mb_az_pat]
kill @e[tag=rlk_mb_az_glyph]
kill @e[type=minecraft:item_display,tag=rlk_az_shard]
schedule clear rlk:boss/azhdaha/prep_glow
data remove storage rlk:mboss az
scoreboard objectives remove azT
scoreboard objectives remove azS
scoreboard objectives remove azPT
scoreboard objectives remove azF
scoreboard objectives remove azBrT
scoreboard objectives remove azBrE
scoreboard objectives remove azBrS
scoreboard objectives remove azBrC
