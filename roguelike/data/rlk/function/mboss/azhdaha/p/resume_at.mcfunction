# A service started at a later clock (#azReqT): PT = it, its reload re-derives the state.
scoreboard players operation #azPT mb = #azReqT mb
scoreboard players set #azReqT mb 0
execute if score #azPat mb matches 20 run return run function rlk:mboss/azhdaha/p/slide/reload
execute if score #azPat mb matches 21 run return run function rlk:mboss/azhdaha/p/absorb1/reload
execute if score #azPat mb matches 22 run return run function rlk:mboss/azhdaha/p/absorb2/reload
execute if score #azPat mb matches 23 run return run function rlk:mboss/azhdaha/p/burrow3/reload
function rlk:mboss/azhdaha/p/start_d
