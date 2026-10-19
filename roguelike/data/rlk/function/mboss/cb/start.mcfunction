# {id} (@s = the zone marker, at it; from cb/spawn_route, #combat = its zid). cur = cbyid.<id> (no roll, no met append,
# never #mbForce), the boss's own arena (fight_vars sets #mbMode 1 and #mbAr from cur). The arena must report built
# (ensure 1): while it does not, cb/wait retries every 10 t (a running or waiting arena job never cancels; 60 retries do).
data remove storage rlk:mboss cur
$data modify storage rlk:mboss cur set from storage rlk:mboss cbyid.$(id)
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_cancel
execute store result score #mbAr mb run data get storage rlk:mboss cur.ar
execute in minecraft:overworld run function rlk:mboss/ar/fl_on
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute in minecraft:overworld unless function rlk:mboss/ar/ensure run return run function rlk:mboss/cb/wait
scoreboard players set #cbWait mb 0
function rlk:mboss/start_go
