# The revive stance (@s = body): she faces the player; lead_re {g:"a13"} when the wait ran out.
function rlk:mboss/mv/turn {max:10}
scoreboard players remove #rvw hr 1
execute if score #rvw hr matches ..0 run function rlk:boss/scarlet/core/lead/re_a13
