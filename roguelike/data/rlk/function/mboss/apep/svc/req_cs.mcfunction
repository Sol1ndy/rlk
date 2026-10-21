# The Heart reached 10000: the CS service (60) now (the stage stops at its t0).
execute if score #apPid mb matches 60 run return 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/apep/p/cancel
scoreboard players set #apPid mb 60
scoreboard players set #apPNew mb 1
scoreboard players set #apReqT mb 0
