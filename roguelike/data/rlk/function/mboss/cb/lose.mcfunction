# Objective loss (callable from anywhere, cm.md 5.8): the normal death path (run/fail, or test/defeat in a test; a Ronova
# revive applies as for any death). #mbLost stays 1 through a revive and is reset by the next fight_vars / cleanup_fight.
scoreboard players set #mbLost mb 1
scoreboard players set @a[tag=player] curHealth 0
