# Test 27: the death (true damage of her whole HP).
execute if score #mbSt mb matches 0 run function rlk:boss/arlecchino/core/intro/done
scoreboard players set #mbTrueEl mb 1
function rlk:mboss/true_pct {pct:100}
