# The skill trigger (core/fp, on_hit flagged #a6q): A6 when the player is within 4.5 b, the phase is older
# than 200 t, it is off cooldown, she is between patterns or in the first 6 t of a windup, 60 %.
scoreboard players set #a6q hr 0
execute if score #ai_pht hr matches ..199 run return fail
execute if score #a6cd hr > #clk hr run return fail
execute if score #pat hr matches 5 run return fail
execute if score #pat hr matches 1.. if score #pt hr matches 7.. run return fail
execute if score #pat hr matches 21.. run return fail
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..4.5] run return fail
execute store result score #t hr run random value 1..100
execute if score #t hr matches 61.. run return fail
execute if score #pat hr matches 1.. run function rlk:boss/scarlet/core/cancel_pat0
function rlk:boss/scarlet/core/start/a6
return 1
