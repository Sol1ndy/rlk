# @s = body: the next action at a decision point (plan 7.4 order).
execute if score #apPid mb matches 1.. run return 0
execute if score #apReq mb matches 1.. run return run function rlk:boss/apep/ai/req
execute if score #mbLock mb matches 1.. run return run function rlk:boss/apep/ai/lock
execute if score #apPh mb matches 1 if score #apTr mb matches 1 run return run function rlk:boss/apep/tr/begin
function rlk:boss/apep/ai/sample
execute if score #apPh mb matches 3 if score #apChP mb matches 1.. run return run function rlk:boss/apep/ai/chain_go
execute if score #apPh mb matches 3 if function rlk:boss/apep/ai/q2_due run return run function rlk:boss/apep/ai/q2_go
execute if score #apPh mb matches 1 if function rlk:boss/apep/ai/back run return 0
execute if score #apPh mb matches 1 unless score #apLastMv mb matches 1 if function rlk:boss/apep/ai/move run return 0
function rlk:boss/apep/ai/pick
