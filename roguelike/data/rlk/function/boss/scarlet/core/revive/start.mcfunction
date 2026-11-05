# The instant death was survived (Ronova's revive; @s = body): the darkness lifted, she stands 8 b from
# the player in her stance; 60 t later lead_stand {g:"a13"} -> A13 again (shield 5/5, the banner).
function rlk:boss/scarlet/core/cancel_d
scoreboard players set #pat hr 0
scoreboard players set #ph hr 8
scoreboard players set #gk hr 2
scoreboard players set #sqn hr 0
scoreboard players set #inv hr 1
tag @s add rlk_mb_inv
function rlk:boss/scarlet/shield/off
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/place8
function rlk:boss/scarlet/rig_stub/look/form/normal
function rlk:boss/scarlet/rig_stub/play/idle2
scoreboard players set #rvw hr 60
