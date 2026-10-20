# A test request (#azReq = pattern / service id; #azReqT = a start clock for services that support it).
scoreboard players operation #azPick mb = #azReq mb
scoreboard players set #azReq mb 0
execute if score #azPick mb matches 31..32 run scoreboard players operation #azCastReq mb = #azPick mb
execute if score #azPick mb matches 31..32 run scoreboard players set #azPick mb 30
function rlk:mboss/azhdaha/ai/lines
scoreboard players operation #azPat mb = #azPick mb
scoreboard players set #azPNew mb 1
