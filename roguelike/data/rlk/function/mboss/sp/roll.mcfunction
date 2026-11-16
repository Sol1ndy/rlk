# From room/rift/arm (@s = the zone marker of a new rift): the special of this rift into rlk:mboss spid (string). Order:
# the test's fixed id rlk:mboss spforce {id} (rift_id / special: used once, cleared here) > a weighted roll over sreg[]
# entries with w >= 1 inside their chapter range and not met this run (spmet) > the same allowing met ones > any w >= 1
# entry (chapter ignored) > sreg[0] (w 0 entries, the test bosses, are only reachable through spforce or this last step).
data remove storage rlk:mboss spid
execute if data storage rlk:mboss spforce.id run function rlk:mboss/sp/roll_force with storage rlk:mboss spforce
data remove storage rlk:mboss spforce
execute if data storage rlk:mboss spid run return 1
scoreboard players set #mbUseMet mb 1
scoreboard players set #mbUseCh mb 1
function rlk:mboss/sp/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseMet mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/sp/roll_pass
execute unless data storage rlk:mboss cand[0] run scoreboard players set #mbUseCh mb 0
execute unless data storage rlk:mboss cand[0] run function rlk:mboss/sp/roll_pass
execute if data storage rlk:mboss cand[0] run function rlk:mboss/sp/roll_pick
execute unless data storage rlk:mboss spid run data modify storage rlk:mboss spid set from storage rlk:mboss sreg[0].id
data remove storage rlk:mboss cand
data remove storage rlk:mboss wq
execute if data storage rlk:mboss spid run return 1
return fail
