# F1 (HR-07, lead decision 11-05): the pending fail of a lethal gauntlet (#grs 5: paused / reloaded after its last
# counting cut with pips left; @s = body, the player back and alive): the gauntlet's fail now (p/<g>/fail: the
# instant death staged, ult/fatal as the player; Ronova's revive applies), then what follows the fatal there: A13 ->
# the revive stance (lead_stand -> A13 again); A8 (ULT60_LETHAL) -> lead_stand {g:"a8"} (its clock held one tick).
scoreboard players set #grs hr 0
execute if score #gk hr matches 2 run function rlk:boss/scarlet/p/a13/fail
execute if score #gk hr matches 2 run return run function rlk:boss/scarlet/core/revive/start
