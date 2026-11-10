# /reload in the counter cinematic: its end (the HP steps it had not applied yet, then CS2 -> the down window, CS3 ->
# the lethal hit -> CS4).
function rlk:boss/scarlet/core/sq/repel/cancel
scoreboard players set #sqn hr 0
function rlk:mboss/cine/end
execute if score #gk hr matches 1 if score #sqh hr matches ..0 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #sqh hr matches ..1 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #sqh hr matches ..2 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #sqh hr matches ..0 run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #sqh hr matches ..1 run function rlk:boss/scarlet/core/hp/pm15
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/kill
function rlk:boss/scarlet/core/down/start
