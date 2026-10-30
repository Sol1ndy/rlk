# /reload: the proxy set again from #apPx (the framework re-spawned the proxies in px.set already).
execute if score #apPx mb matches 0 run return run function rlk:boss/apep/px/p1
execute if score #apPx mb matches 1 run return run function rlk:boss/apep/px/p3u
execute if score #apPx mb matches 2 run return run function rlk:boss/apep/px/p3c
execute if score #apPx mb matches 3 run return run function rlk:boss/apep/px/burrowed
execute if score #apPx mb matches 4 run return run function rlk:boss/apep/px/aloft
execute if score #apPx mb matches 5 run return run function rlk:boss/apep/px/parked
execute if score #apPx mb matches 6 run return run function rlk:boss/apep/px/inv
execute if score #apPx mb matches 7 run return run function rlk:boss/apep/px/dead
function rlk:boss/apep/svc/px_rest
