# burrow3 tick: the B3 clock, the special's tick in the tail window.
scoreboard players operation #azB3T mb = #azPT mb
scoreboard players set #azNoPush mb 1
execute if score #azPT mb matches 59..387 run function rlk:mboss/azhdaha/b3/special_tick
execute if score #azPT mb matches 8..335 run return run function rlk:mboss/azhdaha/p/burrow3/kd/8_335
execute if score #azPT mb matches 360..433 run return run function rlk:mboss/azhdaha/p/burrow3/kd/360_433
