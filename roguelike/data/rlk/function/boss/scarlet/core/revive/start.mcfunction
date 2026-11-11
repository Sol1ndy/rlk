# The instant death was survived (Ronova's revive; @s = body): she stands 8 b from
# the player in her stance; 60 t later lead_re {g:"a13"} -> G2 again (gauge 5/5, the banner).
function rlk:boss/scarlet/core/cancel_d
scoreboard players set #pat hr 0
scoreboard players set #ph hr 8
scoreboard players set #gk hr 2
scoreboard players set #sqn hr 0
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
scoreboard players set #mbBalOff mb 1
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/fx/hud/warn {on:0}
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/place8
function rlk:boss/scarlet/rig/look/form/normal
function rlk:boss/scarlet/rig/play/idle2
scoreboard players set #rvw hr 60
