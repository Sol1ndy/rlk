# Stand-in sequence event (S2b's seq.py has none yet): the clip, 120 t, the beats the core and the tests need.
scoreboard players set #sqdone hr 0
function rlk:boss/scarlet/rig_stub/face/player
execute if score #hrEv hr matches 1 run function rlk:boss/scarlet/rig_stub/play/ev_give
execute unless score #hrEv hr matches 1 run function rlk:boss/scarlet/rig_stub/play/ev_toast
