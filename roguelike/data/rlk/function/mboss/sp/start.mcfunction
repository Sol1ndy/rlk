# {id} (@s = the rift's zone marker, at it). cur = sbyid.<id> (no met append before the fight runs, never #mbForce), the
# special's own arena (fight_vars: #mbMode 1, #mbKind 2, #mbAr). The arena must report built (ensure 1): while it does not,
# sp/wait retries every 10 t (as cb/wait). After start_go: the return point is the rift (sp/ret_rift), spmet += id.
data remove storage rlk:mboss cur
$data modify storage rlk:mboss cur set from storage rlk:mboss sbyid.$(id)
execute unless data storage rlk:mboss cur run return run function rlk:mboss/start_cancel
execute store result score #mbAr mb run data get storage rlk:mboss cur.ar
execute in minecraft:overworld run function rlk:mboss/ar/fl_on
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return run scoreboard players set #spawnT room 10
execute in minecraft:overworld unless function rlk:mboss/ar/ensure run return run function rlk:mboss/sp/wait
function rlk:mboss/start_go
execute unless score #mbOn mb matches 1 run return 0
function rlk:mboss/sp/ret_rift
data modify storage rlk:mboss spmet append from storage rlk:mboss cur.id
