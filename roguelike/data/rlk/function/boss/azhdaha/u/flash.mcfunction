# The hit flash of the hit proxy's part group (manifest proxies.layout flash; 0 = the front group).
execute if score #azFlash mb matches 1 run return run function rlk:boss/azhdaha/rig/flash/head
execute if score #azFlash mb matches 2 run return run function rlk:boss/azhdaha/rig/flash/front
execute if score #azFlash mb matches 3 run return run function rlk:boss/azhdaha/rig/flash/rear
execute if score #azFlash mb matches 4 run return run function rlk:boss/azhdaha/rig/flash/tail
