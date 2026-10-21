# The hit flash of the hit proxy's part group (manifest proxies.layout flash; 0 / a direct body hit = body).
execute if score #apFlash mb matches 1 run return run function rlk:mboss/apep/rig_stub/flash/head
execute if score #apFlash mb matches 2 run return run function rlk:mboss/apep/rig_stub/flash/body
execute if score #apFlash mb matches 3 run return run function rlk:mboss/apep/rig_stub/flash/rear
execute if score #apFlash mb matches 4 run return run function rlk:mboss/apep/rig_stub/flash/tail
execute if score #apFlash mb matches 5 run return run function rlk:mboss/apep/rig_stub/flash/tail
execute if score #apFlash mb matches 6 run return run function rlk:mboss/apep/rig_stub/flash/arms
execute if score #apFlash mb matches 7 run return run function rlk:mboss/apep/rig_stub/flash/arms
execute if score #apFlash mb matches 8 run return run function rlk:mboss/apep/rig_stub/flash/front
execute if score #apFlash mb matches 9 run return run function rlk:mboss/apep/rig_stub/flash/front
execute if score #apFlash mb matches 10 run return run function rlk:mboss/apep/rig_stub/flash/rear
execute if score #apFlash mb matches 11 run return run function rlk:mboss/apep/rig_stub/flash/rear
function rlk:mboss/apep/rig_stub/flash/body
