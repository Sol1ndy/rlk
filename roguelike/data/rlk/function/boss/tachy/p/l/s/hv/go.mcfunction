# L stage hv: tick 0 (@s = body).
scoreboard players set #l_s tk 2
scoreboard players set #l_c tk 0
function rlk:boss/tachy/rig/play/hover_high
execute store result score #l_h tk run random value 80..120
scoreboard players operation #l_q tk = #l_h tk
scoreboard players remove #l_q tk 6
scoreboard players set #l_g tk 30
