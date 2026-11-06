# @s = the new body (from the spawn hook), at it: module state, the rig (p1 look, CROUCH), the withered arena props,
# the entrance (seq/entrance/setup) and its clip; #apTot = the full pool (#mbTot is set right after this hook).
function rlk:boss/apep/ai/consts
function rlk:boss/apep/ai/vars
scoreboard players set #apHide mb -1
scoreboard players set #apPh mb 0
function rlk:boss/apep/rig/init
function rlk:boss/apep/rig/spawn
function rlk:boss/apep/svc/look_p1
function rlk:boss/apep/rig/stance/crouch
function rlk:boss/apep/u/hide_off
function rlk:boss/apep/arena/props_kill
function rlk:boss/apep/arena/props_withered
function rlk:boss/apep/seq/entrance/setup
function rlk:boss/apep/play/entrance_p1
scoreboard players set #apHudQ mb 1
