# E70 interrupted (reload / tests; @s = body): before its brand it is reserved again (P1a, the 70 %
# floor kept); after it the event counts as done (P1b).
execute if score #e70 kn matches 2 run return run function rlk:boss/arlecchino/core/e70_end
tag @s remove rlk_mb_inv
scoreboard players set #e70 kn 0
scoreboard players set #fl kn 1
scoreboard players set #ph kn 1
