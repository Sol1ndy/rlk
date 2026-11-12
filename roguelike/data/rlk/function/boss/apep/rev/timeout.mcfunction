# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
# 2000 t into the stage: the warning, a 파괴 at once and then every 600 t while fewer than
# 2 are alive or coming (time-out spawns ignore the cap).
execute if score #apTo mb matches 0 run function rlk:boss/apep/rev/warn
scoreboard players add #apToT mb 1
execute if score #apToT mb matches 600.. run function rlk:boss/apep/rev/to_spawn
