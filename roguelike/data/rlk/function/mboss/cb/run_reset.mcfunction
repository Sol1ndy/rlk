# From run/start and run/end (also test end): no forced chapter boss, no auto gate press, no per-map chapter state.
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
data remove storage rlk:mboss cprep
data remove storage rlk:mboss cbpeek
# special bosses (Tachy S1): the specials met this run, the test auto-enter (the rift test's force is kept: it may be
# armed before run/start)
function rlk:mboss/sp/run_reset
