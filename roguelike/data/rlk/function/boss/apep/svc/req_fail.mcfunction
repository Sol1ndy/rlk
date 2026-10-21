# The Heart reached 0: the failure strike service (40) now.
execute if score #apPid mb matches 40 run return 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/apep/p/cancel
scoreboard players set #apPid mb 40
scoreboard players set #apPNew mb 1
scoreboard players set #apReqT mb 0
