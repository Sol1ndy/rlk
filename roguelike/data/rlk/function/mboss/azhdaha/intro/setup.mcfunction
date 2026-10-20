# @s = the new body (from the spawn hook), at it: module state, the pair, RES, the rig (geo looks, matte gold),
# the arena props (geo), the intro dressing, the intro clip; HUD.
function rlk:mboss/azhdaha/ai/consts
function rlk:mboss/azhdaha/ai/vars
function rlk:mboss/azhdaha/pair/read
function rlk:mboss/azhdaha/res/apply
function rlk:mboss/azhdaha/rig/init
function rlk:mboss/azhdaha/rig/spawn
function rlk:mboss/azhdaha/look/geo
function rlk:mboss/azhdaha/rig/glow/gold_off
function rlk:mboss/azhdaha/arena/props
scoreboard players set #azArEl mb 5
function rlk:mboss/azhdaha/arena/look_now
function rlk:mboss/azhdaha/seq/intro/setup
function rlk:mboss/azhdaha/rig/play/intro
scoreboard players set #azPh mb 0
scoreboard players set #azHudQ mb 1
function rlk:mboss/azhdaha/hud/refresh
