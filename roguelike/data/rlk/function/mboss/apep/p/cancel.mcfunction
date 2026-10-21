# Stop the main slot now (tests, death, reload, the phase jumps). The pattern's cancel runs as the caller.
execute if score #apPid mb matches 1.. unless score #apPNew mb matches 1 run function rlk:mboss/apep/p/cancel_d
scoreboard players set #apPid mb 0
scoreboard players set #apPNew mb 0
scoreboard players set #apPEnd mb 0
scoreboard players set #apPT mb 0
scoreboard players set #apPRel mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #apYawC mb 0
scoreboard players set #apChP mb 0
scoreboard players set #apNext mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_kept]
kill @e[tag=rlk_mb_ap_pat]
