# The sequence signal (@s = body, right after the tick that set it; api.SIG): repel hp1..hp3 -> the HP step of the
# chain (api.COUNTER_PM per mille of mhpM, true damage; kill = true_pct 100), refill -> shield/arm. Reset to 0.
scoreboard players operation #t hr = #sq_sig hr
scoreboard players set #sq_sig hr 0
execute if score #t hr matches 4 run return run function rlk:boss/scarlet/shield/arm
execute unless score #sqn hr matches 4 run return 0
scoreboard players add #sqh hr 1
execute if score #gk hr matches 1 if score #t hr matches 1 run return run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #t hr matches 2 run return run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 1 if score #t hr matches 3 run return run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #t hr matches 1 run return run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #t hr matches 2 run return run function rlk:boss/scarlet/core/hp/pm15
execute if score #gk hr matches 2 if score #t hr matches 3 run return run function rlk:boss/scarlet/core/kill
