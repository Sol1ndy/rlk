# @s = the new body (from the spawn hook), at it: module state, the pair, RES, the rig (geo looks, matte gold),
# the arena props (geo), the intro dressing, the intro clip; HUD.
function rlk:boss/azhdaha/ai/consts
function rlk:boss/azhdaha/ai/vars
function rlk:boss/azhdaha/pair/read
function rlk:boss/azhdaha/res/apply
function rlk:boss/azhdaha/rig/init
function rlk:boss/azhdaha/rig/spawn
function rlk:boss/azhdaha/look/geo
function rlk:boss/azhdaha/rig/glow/gold_off
function rlk:boss/azhdaha/arena/props
scoreboard players set #azArEl mb 5
function rlk:boss/azhdaha/arena/look_now
function rlk:boss/azhdaha/seq/intro/setup
function rlk:boss/azhdaha/rig/play/intro
scoreboard players set #azPh mb 0
scoreboard players set #azHudQ mb 1
function rlk:boss/azhdaha/hud/refresh
