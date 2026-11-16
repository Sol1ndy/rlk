# From mboss/cleanup (map change, run end, death, room/wipe, uninstall, test stop): no special fight pending, no test
# auto-enter, no prepared rift arena (its forceload went with the cleanup's arena fl_off lines).
scoreboard players set #spOn mb 0
scoreboard players set #spAuto mb 0
data remove storage rlk:mboss sprep
data remove storage rlk:mboss spg
