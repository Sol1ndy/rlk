# Test 27: the death (true damage of her whole HP).
execute if score #mbSt mb matches 0 run function rlk:boss/tachy/core/intro/done
scoreboard players operation #mbTrueEl mb = #el tk
function rlk:mboss/true_pct {pct:100}
