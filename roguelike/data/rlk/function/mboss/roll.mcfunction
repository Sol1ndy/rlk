# Picks rlk:mboss cur (copy of a reg[] entry) and #mbId. Order: #mbForce (tests) > weighted roll over entries
# with w >= 1 inside their chapter range and not met this run > the same allowing met ones > any w >= 1 entry
# (chapter ignored) > reg[0]. Entries with w 0 (test bosses) are only reachable through #mbForce or that last step.
data remove storage rlk:mboss cur
scoreboard players set #mbId mb 0
execute if score #mbForce mb matches 1.. run function rlk:mboss/roll_force
execute if data storage rlk:mboss cur run return run function rlk:mboss/roll_done
scoreboard players set #mbUseMet mb 1
scoreboard players set #mbUseCh mb 1
function rlk:mboss/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseMet mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseCh mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/roll_pass
execute if data storage rlk:mboss cand[0] run function rlk:mboss/roll_pick
execute unless data storage rlk:mboss cur run data modify storage rlk:mboss cur set from storage rlk:mboss reg[0]
function rlk:mboss/roll_done
