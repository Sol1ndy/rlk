# @s = the new body (from the spawn hook), at it: module state, rig in the entrance clip (the cocoon), HUD.
# spawn_hidden: every part starts at scale 0 (spawn would show her for the 3 t blend into the clip).
function rlk:mboss/butterfly/ai/consts
function rlk:mboss/butterfly/ai/vars
function rlk:mboss/butterfly/rig/init
function rlk:mboss/butterfly/rig/spawn_hidden
function rlk:mboss/butterfly/rig/play/entrance
execute positioned ~ ~2.15 ~ run function rlk:mboss/butterfly/rig/prop/cocoon
function rlk:mboss/butterfly/form/hitbox_h
function rlk:mboss/butterfly/hud/refresh
function rlk:mboss/butterfly/seq_h/entrance/setup
