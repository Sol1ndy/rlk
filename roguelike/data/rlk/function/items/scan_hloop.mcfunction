execute unless data storage rlk:scan ids[0] run return 0
data modify storage rlk:scan cur set from storage rlk:scan ids[0]
scoreboard players set #scN tmp 0
function rlk:items/scan_hfetch with storage rlk:scan
execute if score #scN tmp matches 1 run function rlk:items/scan_body
data remove storage rlk:scan ids[0]
function rlk:items/scan_hloop
