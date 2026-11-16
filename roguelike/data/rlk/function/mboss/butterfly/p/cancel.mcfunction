# Stop the slot pattern now (tests, death, reload). Callers run rlk:mboss/lib_clear first when hazards must
# go. The pattern's cancel runs as the caller (the body when it exists): it must use selectors, not @s.
execute if score #bfPat mb matches 1.. unless score #bfPNew mb matches 1 run function rlk:mboss/butterfly/p/cancel_d
scoreboard players set #bfPat mb 0
scoreboard players set #bfPNew mb 0
scoreboard players set #bfPEnd mb 0
scoreboard players set #bfPT mb 0
scoreboard players set #bfPRel mb 0
scoreboard players set #mbNoLeash mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]
kill @e[type=minecraft:marker,tag=rlk_mb_bf_kept]
execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv
