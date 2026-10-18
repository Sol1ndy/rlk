# @s = the new body (from the spawn hook), at it: module state, rig in the entrance clip (the cocoon), HUD.
function rlk:mboss/butterfly/ai/consts
function rlk:mboss/butterfly/ai/vars
function rlk:mboss/butterfly/rig_stub/init
function rlk:mboss/butterfly/rig_stub/spawn
function rlk:mboss/butterfly/rig_stub/play/entrance
function rlk:mboss/butterfly/rig_stub/prop/cocoon
function rlk:mboss/butterfly/form/hitbox_h
function rlk:mboss/butterfly/hud/refresh
# the glowing lime floor disc under the cocoon until the burst
execute positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/p/cocoon_disc {life:80}
