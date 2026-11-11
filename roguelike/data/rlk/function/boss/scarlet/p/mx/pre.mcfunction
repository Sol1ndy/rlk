# MX retreat tick (@s = the body): the clock is held at 0; at its end the iai crouch starts (clip mx from its tick 0).
scoreboard players set #pt hr 0
scoreboard players remove #mx_pre hr 1
function rlk:mboss/mv/face
execute if score #mx_pre hr matches ..0 run function rlk:boss/scarlet/rig/play/mx
