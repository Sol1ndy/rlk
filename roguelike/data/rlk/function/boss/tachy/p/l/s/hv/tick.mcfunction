# L stage hv: one tick (#l_c 1..).
function rlk:boss/tachy/p/l/follow
function rlk:mboss/mv/turn {max:10}
scoreboard players remove #l_g tk 1
execute if score #l_g tk matches ..0 run function rlk:boss/tachy/p/l/glint_t
execute if score #l_c tk = #l_q tk run function rlk:boss/tachy/p/l/cue
execute if score #l_c tk >= #l_h tk run return run function rlk:boss/tachy/p/l/s/dv/go
