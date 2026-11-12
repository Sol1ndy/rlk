# Stop the main slot now (tests, death, reload). The pattern's cancel runs as the caller: selectors only.
execute if score #azPat mb matches 1.. unless score #azPNew mb matches 1 run function rlk:boss/azhdaha/p/cancel_d
scoreboard players set #azPat mb 0
scoreboard players set #azPNew mb 0
scoreboard players set #azPEnd mb 0
scoreboard players set #azPT mb 0
scoreboard players set #azPRel mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #azYawC mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_az_kept]
kill @e[tag=rlk_mb_az_pat]
