# /reload or a pause in the repel: its end state (the HP steps it had not applied yet, then after G1: balance + 3,
# P2; after G2: the lethal hit -> the ending).
function rlk:boss/scarlet/seq/repel/cancel
scoreboard players set #sqn hr 0
function rlk:mboss/cine/end
execute if score #gk hr matches 1 if score #sqh hr matches ..0 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #sqh hr matches ..1 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #sqh hr matches ..2 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #sqh hr matches ..0 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #sqh hr matches ..1 run function rlk:boss/scarlet/core/hp/pm15
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/kill
function rlk:boss/scarlet/core/bal/repel
function rlk:boss/scarlet/core/p2/from_repel
