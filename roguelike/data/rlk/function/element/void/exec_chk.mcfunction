# 소멸 판정 (@s = 몹, combat/apply 에서 #mobHP = 맞은 뒤 체력): 체력 ≤ 최대 체력 × 잠식% 이면 체력 0으로
scoreboard players operation #thr tmp = @s mhpM
scoreboard players operation #thr tmp *= @s rnEr
scoreboard players operation #thr tmp /= #100 tmp
execute if score #mobHP tmp > #thr tmp run return 0
scoreboard players set #mobHP tmp 0
function rlk:element/void/exec_fx
