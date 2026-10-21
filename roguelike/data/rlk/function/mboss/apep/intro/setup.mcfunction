# @s = the new body (from the spawn hook), at it: module state, the rig (p1 look, CROUCH), the withered arena props,
# the entrance (seq/entrance/setup) and its clip; #apTot = the full pool (#mbTot is set right after this hook).
function rlk:mboss/apep/ai/consts
function rlk:mboss/apep/ai/vars
scoreboard players set #apHide mb -1
scoreboard players set #apPh mb 0
function rlk:mboss/apep/rig_stub/init
function rlk:mboss/apep/rig_stub/spawn
function rlk:mboss/apep/svc/look_p1
function rlk:mboss/apep/rig_stub/stance/crouch
function rlk:mboss/apep/u/hide_off
function rlk:mboss/apep/arena/props_kill
function rlk:mboss/apep/arena/props_withered
function rlk:mboss/apep/seq/entrance/setup
function rlk:mboss/apep/play/entrance_p1
scoreboard players set #apHudQ mb 1
