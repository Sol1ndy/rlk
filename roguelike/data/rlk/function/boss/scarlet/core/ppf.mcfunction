# One tick of the perfect-parry flinch (@s = body): she turns to the player; at its end the pattern ends.
function rlk:mboss/mv/turn {max:10}
scoreboard players remove #ppf hr 1
execute if score #ppf hr matches ..0 run function rlk:boss/scarlet/core/pat_end
