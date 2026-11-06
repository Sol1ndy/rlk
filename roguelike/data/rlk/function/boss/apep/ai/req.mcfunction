# A test request (#apReq = a pattern / service id; #apArg / #apNext kept as the test set them).
scoreboard players operation #apPick mb = #apReq mb
scoreboard players set #apReq mb 0
execute if score #apPick mb matches 20 run return run function rlk:boss/apep/tr/begin
function rlk:boss/apep/ai/sample
function rlk:boss/apep/ai/go_raw
