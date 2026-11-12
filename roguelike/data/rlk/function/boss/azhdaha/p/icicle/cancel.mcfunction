# The main-slot part stops (selectors only); the emitter stays when it already holds bg slot T.
execute if score #azBgT mb matches 43 run return 0
kill @e[tag=rlk_mb_az_p43]
scoreboard players set #aq43L mb 0
