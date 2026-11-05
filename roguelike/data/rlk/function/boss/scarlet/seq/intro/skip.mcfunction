# The intro skip (@s = the body; PLAN §3.1): the black falls; under it the intro is cleared (line, the wind, the rock and the
# props, a walk leg in progress), she stands <= 7 b from the player facing them; the core then sets #sq to 553 and the next
# tick plays intro_end from its tick 0 (E10's end pose) with line 11 typed on the black.
function rlk:mboss/mv/stop
execute positioned 884.5 201 0 run kill @e[type=minecraft:item_display,tag=rlk_hr_deco,distance=..1]
function rlk:boss/scarlet/rig/look/props/none
function rlk:mboss/mv/dist
function rlk:boss/scarlet/seq/intro/m/near7
function rlk:boss/scarlet/rig/face/player
