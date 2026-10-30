# @s = body: the next action at a decision point (plan 4.12 order).
execute if score #azPat mb matches 1.. run return 0
execute if score #mbSt mb matches 2 run return 0
execute if score #azReq mb matches 1.. run return run function rlk:boss/azhdaha/ai/req
execute if score #mbLock mb matches 1.. run return run function rlk:boss/azhdaha/ai/lock
execute if score #azTr mb matches 1 run return run function rlk:boss/azhdaha/tr/begin
execute if score #azTr mb matches 2.. run return run function rlk:boss/azhdaha/tr/resume
# (FIX perf) re-sampled unless ai/sample4 ran this tick (the idle step since then is <= 3 degrees)
execute unless score #azQ4 mb matches 0 run function rlk:boss/azhdaha/ai/sample
execute if score #azTailN mb matches 3.. run return run function rlk:boss/azhdaha/ai/stall
execute if score #azBand mb matches 3 if score #azA8 mb matches 1 run function rlk:boss/azhdaha/ai/walk_try
execute if score #azPat mb matches 1.. run return 0
execute if score #azSkipF mb matches 1 run return run function rlk:boss/azhdaha/ai/skipped
execute if function rlk:boss/azhdaha/ai/flank run return 0
function rlk:boss/azhdaha/ai/pick
