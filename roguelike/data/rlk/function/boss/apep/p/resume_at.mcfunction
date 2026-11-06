# A service started at a later clock (#apReqT): PT = it, its reload re-derives the state.
scoreboard players operation #apPT mb = #apReqT mb
scoreboard players set #apReqT mb 0
execute if score #apPid mb matches 40 run return run function rlk:boss/apep/p/fail/reload
function rlk:boss/apep/p/start_d
