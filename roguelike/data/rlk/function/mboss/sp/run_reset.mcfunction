# From mboss/cb/run_reset (run/start, run/end, test end): the specials met this run, the test auto-enter. The rift's own
# run state (#riftUsed) is reset by run/start; a forced rift (#riftForce, spforce) is kept: a test may arm it before
# run/start (the run's first zone then holds the rift).
data modify storage rlk:mboss spmet set value []
scoreboard players set #spAuto mb 0
