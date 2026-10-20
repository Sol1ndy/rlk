# @s = player: back to the arrival spot (cur.start) of the fight in cp_test, the avatar and the fall marker follow.
function rlk:mboss/tp_start with storage rlk:mboss cur.start
function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
# the player moved: the per-tick body position cache (mv/plpos) reads again
scoreboard players set #mbPlG mb -1
