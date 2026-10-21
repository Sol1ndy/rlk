# /reload: the proxy set again from #apPx (the framework re-spawned the proxies in px.set already).
execute if score #apPx mb matches 0 run return run function rlk:mboss/apep/px/p1
execute if score #apPx mb matches 1 run return run function rlk:mboss/apep/px/p3u
execute if score #apPx mb matches 2 run return run function rlk:mboss/apep/px/p3c
execute if score #apPx mb matches 3 run return run function rlk:mboss/apep/px/burrowed
execute if score #apPx mb matches 4 run return run function rlk:mboss/apep/px/aloft
execute if score #apPx mb matches 5 run return run function rlk:mboss/apep/px/inv
execute if score #apPx mb matches 6 run return run function rlk:mboss/apep/px/parked
execute if score #apPx mb matches 7 run return run function rlk:mboss/apep/px/dead
function rlk:mboss/apep/svc/px_rest
